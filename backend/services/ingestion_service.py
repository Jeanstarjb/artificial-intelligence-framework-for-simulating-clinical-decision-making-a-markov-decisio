from datetime import datetime
from typing import Dict, Any
from pydantic import ValidationError
import numpy as np
from schemas import EHRData, PatientCreate

class DataPreprocessor:
    @staticmethod
    def transform_fhir_to_internal(ehr_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert FHIR format to internal data model"""
        return {
            "medical_record_number": ehr_data['id'],
            "name": f"{ehr_data['name']['given'][0]} {ehr_data['name']['family']}",
            "age": datetime.now().year - datetime.strptime(ehr_data['birthDate'], '%Y-%m-%d').year,
            "gender": ehr_data['gender'].capitalize(),
            "medical_history": [c['code']['text'] for c in ehr_data['conditions']],
            "current_medications": [m['medication']['text'] for m in ehr_data['medications']],
            "vital_signs": {
                "heart_rate": next((v['valueQuantity']['value'] for v in ehr_data['observations'] 
                                  if v['code']['coding'][0]['code'] == '8867-4'), None),
                "blood_pressure": next((f"{v['valueQuantity']['value']} mmHg" for v in ehr_data['observations']
                                       if v['code']['coding'][0]['code'] == '85354-9'), None)
            }
        }

    @staticmethod
    def handle_missing_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Impute missing values and track data quality"""
        imputations = {}
        
        # Age imputation
        if 'age' not in raw_data or not raw_data['age']:
            imputations['age'] = np.median([p['age'] for p in Patient.query.all()])
            
        # Default gender if missing
        raw_data.setdefault('gender', 'Unknown')
        
        return raw_data, imputations

def validate_patient_data(raw_data: Dict[str, Any]) -> EHRData:
    try:
        return EHRData(**raw_data)
    except ValidationError as e:
        raise ValueError(f"Data validation error: {str(e)}")

async def preprocess_ehr_data(ehr_data: EHRData) -> PatientCreate:
    preprocessor = DataPreprocessor()
    raw_data = preprocessor.transform_fhir_to_internal(ehr_data.dict())
    cleaned_data, imputations = preprocessor.handle_missing_data(raw_data)
    return PatientCreate(**cleaned_data)