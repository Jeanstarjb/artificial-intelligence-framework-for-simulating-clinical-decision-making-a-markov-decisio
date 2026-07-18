from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models import Patient
from database import get_db
from services.ingestion_service import preprocess_ehr_data, validate_patient_data
from schemas import EHRData, DataQualityReport
import logging

router = APIRouter(prefix="/api/ingest", tags=["Data Ingestion"])
logger = logging.getLogger(__name__)

@router.post("/ehr", response_model=DataQualityReport)
async def ingest_ehr_data(
    ehr_payload: EHRData,
    db: AsyncSession = Depends(get_db)
):
    try:
        # Validate and preprocess data
        validated_data = validate_patient_data(ehr_payload.dict())
        processed_patient = preprocess_ehr_data(validated_data)
        
        # Create database record
        db_patient = Patient(**processed_patient.dict())
        db.add(db_patient)
        await db.commit()
        await db.refresh(db_patient)
        
        return {
            "status": "success",
            "missing_fields": validated_data.missing_fields,
            "imputed_values": validated_data.imputed_values,
            "patient_id": str(db_patient.id)
        }
    
    except Exception as e:
        logger.error(f"Ingestion failed: {str(e)}", exc_info=True)
        await db.rollback()
        raise HTTPException(status_code=422, detail=str(e))