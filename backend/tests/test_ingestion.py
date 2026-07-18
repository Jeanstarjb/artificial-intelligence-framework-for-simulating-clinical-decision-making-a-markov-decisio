import pytest
from fastapi.testclient import TestClient
from main import app
from services.ingestion_service import DataPreprocessor
from schemas import EHRData
import datetime

@pytest.fixture
def sample_ehr_data():
    return {
        "resourceType": "Patient",
        "id": "MRN12345",
        "name": {"family": "Doe", "given": ["John"]},
        "gender": "male",
        "birthDate": "1980-05-15",
        "conditions": [{"code": {"coding": [{"code": "I10"}], "text": "Hypertension"}}],
        "medications": [{"medication": {"text": "Lisinopril 10mg"}}],
        "observations": [
            {"code": {"coding": [{"code": "8867-4"}]}, "valueQuantity": {"value": 72}},
            {"code": {"coding": [{"code": "85354-9"}]}, "valueQuantity": {"value": "120/80"}}
        ]
    }


def test_fhir_transformation(sample_ehr_data):
    preprocessor = DataPreprocessor()
    result = preprocessor.transform_fhir_to_internal(sample_ehr_data)
    
    assert result["medical_record_number"] == "MRN12345"
    assert result["name"] == "John Doe"
    assert result["age"] == datetime.datetime.now().year - 1980
    assert "Hypertension" in result["medical_history"]
    assert result["vital_signs"]["heart_rate"] == 72


def test_ingestion_endpoint():
    client = TestClient(app)
    response = client.post("/api/ingest/ehr", json={
        "resourceType": "Patient",
        "id": "TEST123",
        "name": {"family": "Smith", "given": ["Alice"]},
        "gender": "female",
        "birthDate": "1995-01-01",
        "conditions": [],
        "medications": [],
        "observations": [
            {"code": {"coding": [{"code": "8867-4"}]}, "valueQuantity": {"value": 65}},
            {"code": {"coding": [{"code": "85354-9"}]}, "valueQuantity": {"value": "110/70"}}
        ]
    })
    
    assert response.status_code == 200
    assert "patient_id" in response.json()