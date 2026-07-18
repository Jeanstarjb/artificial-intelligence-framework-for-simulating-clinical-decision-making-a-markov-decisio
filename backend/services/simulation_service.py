from typing import Dict, Any, List
from .ddn_engine import ClinicalDDN, BeliefState
from .mdp_engine import ClinicalMDP
from .policy_evaluator import PolicyEvaluator
from schemas import SimulationResult, DDNSimulationParameters
import numpy as np

async def simulate_treatment_paths(
    patient_data: Dict[str, Any],
    params: DDNSimulationParameters
) -> SimulationResult:
    # Initialize models
    mdp = create_clinical_mdp(patient_data)
    ddn = ClinicalDDN(
        states=patient_data['possible_states'],
        actions=patient_data['available_treatments'],
        observations=patient_data['possible_observations'],
        transition_model=patient_data['transition_model'],
        observation_model=patient_data['observation_model'],
        reward_model=patient_data['reward_model'],
        discount=params.discount_factor
    )
    
    evaluator = PolicyEvaluator(mdp, ddn)
    
    # Run simulations based on type
    if params.simulation_type == 'mdp':
        policy = mdp.extract_optimal_policy()
        evaluation = evaluator.evaluate_mdp_policy(
            policy,
            n_simulations=params.monte_carlo_runs
        )
    else:
        initial_belief = BeliefState.parse_obj(patient_data['initial_belief'])
        evaluation = evaluator.ddn_policy_analysis(
            initial_belief,
            horizon=params.horizon_steps
        )
    
    # Comparative analysis
    policies = [
        {'name': 'current_guidelines', 'type': 'ddn', 'strategy': 'clinical_guidelines'},
        {'name': 'mdp_optimal', 'type': 'mdp', 'strategy': 'value_iteration'},
        {'name': 'ddn_adaptive', 'type': 'ddn', 'strategy': 'optimal'}
    ]
    comparison = evaluator.compare_policies(patient_data, policies)

    return SimulationResult(
        optimal_policy=evaluation.get('optimal_policy', {}),
        value_estimates={
            'qaly': evaluation['value_estimate'],
            'cost': evaluation.get('cost_estimate', 0)
        },
        probabilistic_outcomes={
            'success_probability': evaluation['policy_comparison']['ddn_adaptive']['mean_reward'],
            'qaly_distribution': evaluation['qaly_distribution']
        },
        sensitivity_analysis=comparison['sensitivity_analysis'],
        clinical_metrics={
            'estimated_qaly_gain': comparison['cost_effectiveness']['qaly'],
            'cost_per_qaly': comparison['cost_effectiveness']['icer']
        },
        simulation_metadata={
            'model_type': params.simulation_type,
            'run_id': generate_simulation_id(),
            'timestamp': datetime.utcnow().isoformat()
        }
    )

def generate_simulation_id() -> str:
    return f"SIM_{int(datetime.utcnow().timestamp())}_{np.random.randint(1000,9999)}"

def create_clinical_mdp(patient_data: Dict) -> ClinicalMDP:
    return ClinicalMDP(
        states=patient_data['possible_states'],
        actions=patient_data['available_treatments'],
        transition_probs=patient_data['transition_model'],
        rewards=patient_data['reward_model'],
        gamma=0.9
    )
