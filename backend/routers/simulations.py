from fastapi import APIRouter, Depends
from schemas import DDNSimulationParameters, SimulationResult
from services.simulation_service import simulate_treatment_paths
from database import get_db
from models import Patient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

router = APIRouter(prefix="/api/simulate", tags=["Decision Simulation"])

@router.post("/{patient_id}", response_model=SimulationResult)
async def run_simulation(
    patient_id: str,
    params: DDNSimulationParameters,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Patient).filter(Patient.id == patient_id))
    patient = result.scalars().first()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return await simulate_treatment_paths(
        patient_data=patient.vital_signs,
        params=params
    )