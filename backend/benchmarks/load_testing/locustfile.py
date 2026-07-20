from locust import HttpUser, task, between
import numpy as np

class CDSSLoadTest(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def test_recommendation_endpoint(self):
        patient_data = {
            "patient_id": "test_123",
            "patient_data": {
                "age": np.random.randint(18, 90),
                "diagnosis": np.random.choice(['hypertension', 'diabetes', 'copd']),
                "lab_results": {
                    "hr": np.random.normal(80, 20),
                    "bp": f"{np.random.randint(90, 180)}/{np.random.randint(60, 120)}"
                }
            },
            "model_parameters": {"urgency": "high"}
        }
        self.client.post("/api/recommendations/", json=patient_data)

    @task(3)
    def test_simulation_endpoint(self):
        sim_params = {
            "patient_id": "test_123",
            "horizon": 5,
            "n_simulations": 1000,
            "risk_tolerance": 0.3
        }
        self.client.post("/api/simulate/test_123", json=sim_params)