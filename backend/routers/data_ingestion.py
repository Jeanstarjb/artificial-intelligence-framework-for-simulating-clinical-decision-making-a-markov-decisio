from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from models import Patient, EHRWebhookLog
from database import get_db
from services.ingestion_service import preprocess_ehr_data, validate_patient_data
from services.ehr_sync_service import process_webhook_payload
from services.security import verify_webhook_signature
from schemas import EHRData, DataQualityReport, EHRWebhookPayload, EHRWebhookLogSchema
import logging
import json
from json import JSONDecodeError
from datetime import datetime

router = APIRouter(prefix="/api/ingest", tags=["Data Ingestion"])
logger = logging.getLogger(__name__)

@router.post("/webhook", status_code=202, response_model=EHRWebhookLogSchema)
async def ehr_webhook_handler(
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    payload_body = await request.body()
    signature_header = request.headers.get("X-EHR-Signature")
    
    if not signature_header:
        raise HTTPException(status_code=400, detail="Missing X-EHR-Signature header")
    
    verify_webhook_signature(payload_body, signature_header)
    
    try:
        payload = json.loads(payload_body)
    except JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    
    webhook_log = EHRWebhookLog(
        received_at=datetime.utcnow(),
        status='processing',
        payload_size=len(payload_body),
        processed_entries=0,
        patient_ids=[]
    )
    db.add(webhook_log)
    await db.commit()
    await db.refresh(webhook_log)
    
    background_tasks.add_task(process_webhook_payload, payload, webhook_log.id)
    
    return webhook_log