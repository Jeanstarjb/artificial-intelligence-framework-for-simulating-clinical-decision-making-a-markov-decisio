from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import engine, Base
from routers import patients, simulations
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="CDSS Core API",
    description="Clinical Decision Support Engine",
    version="0.2.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patients.router)
app.include_router(simulations.router)

@app.get("/health")
async def health_check():
    return {
        "status": "operational",
        "version": {
            "engine": "MDP v2.3",
            "model": "clinical-path-optimizer"
        }
    }
