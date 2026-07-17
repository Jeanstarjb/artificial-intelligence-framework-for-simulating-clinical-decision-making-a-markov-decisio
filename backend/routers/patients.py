from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from models import Patient
from schemas import PatientResponse
from database import get_db
from sqlalchemy.future import select

router = APIRouter(prefix="/api/patients", tags=["Patient Data"])

@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(patient_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Patient).filter(Patient.id == patient_id))
    patient = result.scalars().first()
    return patient

@router.get("/search", response_model=list[PatientResponse])
async def search_patients(
    name: Optional[str] = Query(None),
    age_min: Optional[int] = Query(None),
    age_max: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    query = select(Patient)
    if name:
        query = query.filter(Patient.name.ilike(f"%{name}%"))
    if age_min is not None:
        query = query.filter(Patient.age >= age_min)
    if age_max is not None:
        query = query.filter(Patient.age <= age_max)
    
    result = await db.execute(query)
    return result.scalars().all()
