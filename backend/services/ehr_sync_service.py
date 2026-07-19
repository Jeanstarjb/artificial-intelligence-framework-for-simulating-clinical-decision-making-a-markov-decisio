from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from models import Patient, EHRWebhookLog
from services.ingestion_service import DataPreprocessor
from database import AsyncSessionLocal
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

async def process_webhook_payload(payload: dict, log_id: str):
    async with AsyncSessionLocal() as db:
        try:
            log = await db.get(EHRWebhookLog, log_id)
            if not log:
                logger.error(f"Webhook log {log_id} not found")
                return
            
            processed_entries = 0
            patient_ids = []
            
            for entry in payload.get('entries', []):
                try:
                    preprocessed = DataPreprocessor.transform_fhir_to_internal(entry)
                    stmt = pg_insert(Patient).\
                        values(**preprocessed).\
                        on_conflict_do_update(
                            index_elements=['medical_record_number'],
                            set_=preprocessed
                        ).\
                        returning(Patient.id)
                    result = await db.execute(stmt)
                    patient_id = result.scalar()
                    patient_ids.append(str(patient_id))
                    processed_entries += 1
                except Exception as e:
                    logger.error(f"Entry processing failed: {str(e)}")
                    continue
            
            log.status = 'processed' if processed_entries == len(payload.get('entries', [])) else 'partial_error'
            log.processed_entries = processed_entries
            log.patient_ids = patient_ids
            await db.commit()
        except Exception as e:
            logger.error(f"Webhook processing failed: {str(e)}")
            if log:
                log.status = 'error'
                log.error_message = str(e)
                await db.commit()