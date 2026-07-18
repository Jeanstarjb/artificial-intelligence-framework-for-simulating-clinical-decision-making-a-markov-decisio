from schemas import SimulationResult
from .mdp_engine import create_clinical_mdp
from .ddn_engine import ClinicalDDN, BeliefState
from typing import Dict, Any

async def simulate_treatment_paths(
    patient_data: Dict[str, Any],
    params: DDNSimulationParameters
) -> SimulationResult:
    # Initialize DDN with clinical models
    ddn = ClinicalDDN(
        states=patient_data['possible_states'],
        actions=patient_data['available_treatments'],
        observations=patient_data['possible_observations'],
        transition_model=patient_data['transition_model'],
        observation_model=params.observation_model,
        reward_model=patient_data['reward_model'],
        discount=params.discount_factor
    )

    initial_belief = BeliefState(probabilities=params.initial_belief)
    treatment_path = ddn.generate_optimal_path(initial_belief, params.horizon)

    expected_utility = sum(
        step['reward'] * (params.discount_factor ** i)
        for i, step in enumerate(treatment_path)
    )

    return SimulationResult(
        optimal_path=treatment_path,
        expected_utility=expected_utility,
        belief_states=[BeliefState(**step['belief_state']) for step in treatment_path]
    )