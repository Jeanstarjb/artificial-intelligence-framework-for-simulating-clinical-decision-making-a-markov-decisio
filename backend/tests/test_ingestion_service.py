import pytest
from services.ingestion_service import DataPreprocessor
from schemas import EHRData
from pydantic import ValidationError

def test_fhir_transformation():
    fhir_data = {
        "id": "12345",
        "name": {"given": ["John"], "family": "Doe"},
        "birthDate": "1980-05-15",
        "gender": "male",
        "address": [{"line": ["123 Main St"], "city": "Anytown"}]
    }
    
 = DataPreprocessor.transform_fhir_to_internal(fhir_data)
    
    assert transformed['medical_record_number'] == "12345"
    assert transformed['first_name'] == "John"
    assert transformed['date_of_birth'].year == 1980

def test_invalid_patient_data():
    invalid_data = {
        "medical_record_number": "123",
        "first_name": "A" * 51,
        "gender": "invalid"
    }
    
    with pytest.raises(ValidationError):
        DataPreprocessor.validate_patient_data(invalid_data)

def test_data_quality_report():
    incomplete_data = {
        "medical_record_number": "67890",
        "first_name": "Jane"
    }
    report = DataPreprocessor.generate_quality_report(incomplete_data)
    
    assert report.missing_fields == ['last_name', 'date_of_birth', 'gender']
    assert not report.is_valid