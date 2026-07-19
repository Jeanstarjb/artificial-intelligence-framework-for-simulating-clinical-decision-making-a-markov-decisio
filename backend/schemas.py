from pydantic import BaseModel
from typing import List, Dict

class RecommendationRequest(BaseModel):
    patient_id: str
    patient_data: Dict[str, any]
    model_parameters: Dict[str, any] = {}

class TreatmentRecommendation(BaseModel):
    treatment: str
    confidence: float
    rationale: str

class RecommendationResponse(BaseModel):
    patient_id: str
    recommendations: List[TreatmentRecommendation]
    model_version: str
    confidence_threshold: float