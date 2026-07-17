from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database import Base
import datetime

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(UUID(as_uuid=True), primary_key=True)
    medical_record_number = Column(String(50), unique=True)
    name = Column(String(100))
    age = Column(Integer)
    gender = Column(String(25))
    medical_history = Column(JSON)
    current_medications = Column(JSON)
    vital_signs = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)
