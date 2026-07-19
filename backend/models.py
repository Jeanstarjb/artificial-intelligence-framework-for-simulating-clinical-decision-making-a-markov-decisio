from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Text, Index, text, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    medical_record_number = Column(String(50), unique=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    date_of_birth = Column(DateTime)
    gender = Column(String(25))
    last_updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    # ... other existing columns ...

class EHRWebhookLog(Base):
    __tablename__ = 'ehr_webhook_logs'
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    received_at = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False)
    payload_size = Column(Integer, nullable=False)
    processed_entries = Column(Integer, default=0)
    patient_ids = Column(ARRAY(String(50)))
    error_message = Column(Text)