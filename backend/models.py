from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Text, Index, text
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
    medical_history = Column(JSONB)
    current_medications = Column(JSONB)
    vital_signs = Column(JSONB)
    lab_results = Column(JSONB)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    simulations = relationship('Simulation', back_populates='patient')

    __table_args__ = (
        Index('ix_patient_medical_record', 'medical_record_number', postgresql_using='hash'),
    )

class Simulation(Base):
    __tablename__ = 'simulations'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    patient_id = Column(UUID(as_uuid=True), ForeignKey('patients.id'))
    parameters = Column(JSONB)
    status = Column(String(20), default='pending')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime)
    patient = relationship('Patient', back_populates='simulations')
    evaluations = relationship('PolicyEvaluation', back_populates='simulation')

    __table_args__ = (
        Index('ix_simulation_patient', 'patient_id'),
        Index('ix_simulation_status', 'status'),
        Index('gin_simulation_parameters', 'parameters', postgresql_using='gin')
    )

class PolicyEvaluation(Base):
    __tablename__ = 'policy_evaluations'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    simulation_id = Column(UUID(as_uuid=True), ForeignKey('simulations.id'))
    optimal_actions = Column(JSONB)
    value_function = Column(JSONB)
    qaly_estimate = Column(Integer)
    cost_effectiveness = Column(JSONB)
    confidence_intervals = Column(JSONB)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    simulation = relationship('Simulation', back_populates='evaluations')

    __table_args__ = (
        Index('ix_policy_eval_simulation', 'simulation_id'),
        Index('gin_policy_eval_actions', 'optimal_actions', postgresql_using='gin')
    )

class ModelVersion(Base):
    __tablename__ = 'model_versions'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    model_type = Column(String(20))  # MDP/DDN
    version = Column(String(50))
    parameters = Column(JSONB)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Integer, default=1)

    __table_args__ = (
        Index('ix_model_type_version', 'model_type', 'version'),
        Index('ix_model_active', 'is_active')
    )

class Treatment(Base):
    __tablename__ = 'treatments'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    patient_id = Column(UUID(as_uuid=True), ForeignKey('patients.id'))
    simulation_id = Column(UUID(as_uuid=True), ForeignKey('simulations.id'))
    treatment_data = Column(JSONB)
    outcome = Column(JSONB)
    administered_at = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        Index('ix_treatment_patient', 'patient_id'),
        Index('ix_treatment_simulation', 'simulation_id'),
        Index('gin_treatment_data', 'treatment_data', postgresql_using='gin')
    )

class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    user_id = Column(String(50))
    action = Column(String(50))
    table_name = Column(String(50))
    record_id = Column(UUID(as_uuid=True))
    previous_state = Column(JSONB)
    new_state = Column(JSONB)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        Index('ix_audit_user', 'user_id'),
        Index('ix_audit_table', 'table_name'),
        Index('ix_audit_timestamp', 'timestamp')
    )
