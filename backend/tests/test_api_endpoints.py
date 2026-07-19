import pytest
from fastapi import status
from schemas import PatientResponse, SimulationResult, RecommendationResponse

@pytest.mark.asyncio
async def test_get_patient(client):
    response = client.get("/api/patients/invalid_id")
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_simulation_endpoint(client):
    test_data = {
        "horizon": 5,
        "discount_factor": 0.9,
        "max_iterations": 100
    }
    response = client.post("/api/simulate/patient123", json=test_data)
    assert response.status_code == status.HTTP_200_OK
    assert SimulationResult(**response.json())

@pytest.mark.asyncio
async def test_recommendation_endpoint(client):
    test_data = {
        "patient_id": "patient123",
        "patient_data": {"age": 45, "condition": "diabetes"},
        "model_parameters": {"confidence_threshold": 0.8}
    }
    response = client.post("/api/recommendations/", json=test_data)
    assert response.status_code == status.HTTP_200_OK
    assert RecommendationResponse(**response.json())