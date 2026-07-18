from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional
from datetime import date

class EHRData(BaseModel):
    """FHIR-compatible input schema"""
    resourceType: str = Field(..., example="Patient")
    id: str = Field(..., description="Medical record number")
    name: Dict[str, List[str]] = Field(..., example={"family": "Smith", "given": ["John"]})
    gender: str = Field(..., regex="^(male|female|other|unknown)$")
    birthDate: date
    conditions: List[Dict] = Field(..., description="List of condition resources")
    medications: List[Dict] = Field(..., description="Current medications")
    observations: List[Dict] = Field(..., description="Vital signs and measurements")

    @validator('observations')
    def validate_observations(cls, v):
        required_codes = {'8867-4', '85354-9'}
        found_codes = {obs['code']['coding'][0]['code'] for obs in v}
        if not required_codes.issubset(found_codes):
            raise ValueError("Missing required vital sign measurements")
        return v

class DataQualityReport(BaseModel):
    status: str
    missing_fields: List[str] = []
    imputed_values: Dict[str, float] = {}
    patient_id: Optional[str] = None

class PatientCreate(BaseModel):
    medical_record_number: str
    name: str
    age: int
    gender: str
    medical_history: List[str]
    current_medications: List[str]
    vital_signs: Dict[str, Any]