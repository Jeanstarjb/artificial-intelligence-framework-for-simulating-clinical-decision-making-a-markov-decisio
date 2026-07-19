import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from typing import Dict, List, Tuple
import optuna
from models import Patient
from database import get_db

class PatientDataset(Dataset):
    def __init__(self, features, labels):
        self.features = torch.FloatTensor(features)
        self.labels = torch.FloatTensor(labels)

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]

class PersonalizedMedicineModel(nn.Module):
    def __init__(self, input_dim, output_dim, hidden_dims=[256, 128], dropout=0.2):
        super().__init__()
        layers = []
        prev_dim = input_dim
        for dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, dim))
            layers.append(nn.BatchNorm1d(dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout))
            prev_dim = dim
        layers.append(nn.Linear(prev_dim, output_dim))
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return torch.sigmoid(self.net(x))

class RecommendationEngine:
    def __init__(self, db_session):
        self.db = db_session
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.scaler = StandardScaler()
        self.label_encoder = {}
        self.model = None

    async def load_patient_data(self):
        result = await self.db.execute(
            text('''
                SELECT p.id, p.age, p.gender, p.medical_history, 
                    ARRAY_AGG(d.medication) as previous_treatments,
                    AVG(v.value_numeric) as avg_biomarker
                FROM patients p
                LEFT JOIN diagnoses d ON p.id = d.patient_id
                LEFT JOIN vital_signs v ON p.id = v.patient_id
                GROUP BY p.id
            ''')
        )
        return result.fetchall()

    def preprocess_data(self, raw_data):
        # Feature engineering and normalization
        processed = []
        for row in raw_data:
            features = [
                row.age,
                1 if row.gender == 'male' else 0,
                len(row.medical_history),
                len(row.previous_treatments),
                row.avg_biomarker or 0
            ]
            processed.append(features)
        return self.scaler.fit_transform(np.array(processed))

    def train_model(self, X, y, n_trials=50):
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)

        def objective(trial):
            params = {
                'hidden_dims': [
                    trial.suggest_int('n_units_l1', 64, 256),
                    trial.suggest_int('n_units_l2', 32, 128)
                ],
                'lr': trial.suggest_float('lr', 1e-4, 1e-2, log=True),
                'batch_size': trial.suggest_categorical('batch_size', [32, 64, 128]),
                'dropout': trial.suggest_float('dropout', 0.1, 0.5)
            }

            model = PersonalizedMedicineModel(
                input_dim=X.shape[1],
                output_dim=y.shape[1],
                hidden_dims=params['hidden_dims'],
                dropout=params['dropout']
            ).to(self.device)

            train_loader = DataLoader(
                PatientDataset(X_train, y_train),
                batch_size=params['batch_size'],
                shuffle=True
            )

            optimizer = optim.Adam(model.parameters(), lr=params['lr'])
            criterion = nn.BCELoss()

            for epoch in range(50):
                for inputs, labels in train_loader:
                    inputs = inputs.to(self.device)
                    labels = labels.to(self.device)
                    optimizer.zero_grad()
                    outputs = model(inputs)
                    loss = criterion(outputs, labels)
                    loss.backward()
                    optimizer.step()

            with torch.no_grad():
                val_outputs = model(torch.FloatTensor(X_val).to(self.device))
                val_loss = criterion(val_outputs, torch.FloatTensor(y_val).to(self.device))
            return val_loss.item()

        study = optuna.create_study(direction='minimize')
        study.optimize(objective, n_trials=n_trials)
        self.model = PersonalizedMedicineModel(
            input_dim=X.shape[1],
            output_dim=y.shape[1],
            hidden_dims=study.best_params['n_units_l1', 'n_units_l2'],
            dropout=study.best_params['dropout']
        ).to(self.device)

    async def recommend_treatments(self, patient_data: Dict) -> List[Tuple[str, float]]:
        if not self.model:
            raw_data = await self.load_patient_data()
            X = self.preprocess_data(raw_data)
            y = np.array([[1 if t in row.previous_treatments else 0 for t in self.treatments] 
                         for row in raw_data])
            self.train_model(X, y)

        processed_input = self.scaler.transform([
            patient_data['age'],
            1 if patient_data['gender'] == 'male' else 0,
            len(patient_data['medical_history']),
            len(patient_data['previous_treatments']),
            patient_data.get('latest_biomarker', 0)
        ])

        with torch.no_grad():
            inputs = torch.FloatTensor(processed_input).to(self.device)
            outputs = self.model(inputs).cpu().numpy()[0]

        return sorted(zip(self.treatments, outputs), 
                   key=lambda x: x[1], reverse=True)[:5]