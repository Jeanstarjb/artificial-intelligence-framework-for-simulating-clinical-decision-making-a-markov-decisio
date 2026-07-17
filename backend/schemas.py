from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PatientResponse(BaseModel):
    id: str
    medical_record_number: str
    name: str
    age: int
    gender: str
    medical_history: dict
    current_medications: dict
    vital_signs: dict
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class SimulationParameters(BaseModel):
    horizon: int = 5
    discount_factor: float = 0.9
    max_iterations: int = 1000

class SimulationResult(BaseModel):
    optimal_path: List[dict]
    expected_utility: float
    confidence_interval: tuple
    risk_assessment: dict
