from datetime import datetime
from typing import Dict, Any
from pydantic import ValidationError
import numpy as np
from schemas import EHRData, PatientCreate

class DataPreprocessor:
    @staticmethod
    def transform_fhir_to_internal(ehr_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "medical_record_number": ehr_data['id'],
            "first_name": ehr_data['name']['given'][0],
            "last_name": ehr_data['name']['family'],
            "date_of_birth": datetime.strptime(ehr_data['birthDate'], '%Y-%m-%d'),
            "gender": ehr_data['gender'],
            # ... other transformed fields ...
        }