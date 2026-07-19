from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_db
from services.recommendation_service import RecommendationEngine
from schemas import RecommendationResponse, RecommendationRequest
import numpy as np

router = APIRouter(prefix="/api/recommendations", tags=["Treatment Recommendations"])

def get_recommendation_engine(db: AsyncSession = Depends(get_db)):
    return RecommendationEngine(db)

@router.post("/", response_model=RecommendationResponse)
async def get_recommendations(
    request: RecommendationRequest,
    engine: RecommendationEngine = Depends(get_recommendation_engine)
):
    try:
        recommendations = await engine.recommend_treatments(request.patient_data)
        return {
            "patient_id": request.patient_id,
            "recommendations": [{
                "treatment": t[0],
                "confidence": float(t[1]),
                "rationale": f"Recommended based on patient age {request.patient_data['age']} "
                             f"with {len(request.patient_data['medical_history'])} documented conditions"
            } for t in recommendations],
            "model_version": "1.0.0",
            "confidence_threshold": 0.7
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Recommendation failed: {str(e)}"
        )