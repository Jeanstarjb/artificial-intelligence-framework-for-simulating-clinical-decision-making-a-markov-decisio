from fastapi import APIRouter, Depends
from schemas import SimulationParameters, SimulationResult
from services.simulation_service import simulate_treatment_paths
from database import get_db
from models import Patient
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/simulate", tags=["Decision Simulation"])

@router.post("/{patient_id}", response_model=SimulationResult)
async def run_simulation(
    patient_id: str,
    params: SimulationParameters,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Patient).filter(Patient.id == patient_id))
    patient = result.scalars().first()
    
    simulation_result = await simulate_treatment_paths(
        patient_data=patient,
        horizon=params.horizon,
        discount_factor=params.discount_factor,
        max_iterations=params.max_iterations
    )
    return simulation_result
