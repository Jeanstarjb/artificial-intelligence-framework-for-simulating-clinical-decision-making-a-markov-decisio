from schemas import SimulationResult
from .mdp_engine import create_clinical_mdp
from typing import Dict, Any

async def simulate_treatment_paths(
    patient_data: Dict[str, Any],
    horizon: int = 5,
    discount_factor: float = 0.9,
    max_iterations: int = 1000
) -> SimulationResult:
    mdp = create_clinical_mdp(patient_data)
    initial_state = determine_initial_state(patient_data)
    treatment_path = mdp.generate_treatment_path(initial_state, horizon)
    
    expected_utility = sum(step['reward'] * (discount_factor ** i) 
                          for i, step in enumerate(treatment_path))
    
    return SimulationResult(
        optimal_path=treatment_path,
        expected_utility=expected_utility
    )

def determine_initial_state(patient_data: Dict) -> str:
    vitals = patient_data.get('vital_signs', {})
    if vitals.get('heart_rate', 0) > 120 or vitals.get('bp_systolic', 0) > 180:
        return "critical"
    if patient_data.get('medical_history', {}).get('chronic_conditions', []):
        return "stable"
    return "improving"