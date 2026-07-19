from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

class EHRWebhookPayload(BaseModel):
    entries: List[Dict[str, Any]]

class EHRWebhookLogSchema(BaseModel):
    received_at: datetime
    status: str
    payload_size: int
    processed_entries: int
    patient_ids: List[str]
    error_message: Optional[str] = None

    class Config:
        orm_mode = True