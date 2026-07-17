import pytest
from services.mdp_engine import ClinicalMDP, create_clinical_mdp

@pytest.fixture
def sample_mdp() -> ClinicalMDP:
    states = ['s1', 's2']
    actions = ['a1', 'a2']
    transition_probs = {
        's1': {'a1': {'s2': 1.0}, 'a2': {'s1': 1.0}},
        's2': {'a1': {'s2': 1.0}, 'a2': {'s1': 1.0}}
    }
    rewards = {'s1': {'a1': 5.0}, 's2': {'a1': -1.0}}
    return ClinicalMDP(states, actions, transition_probs, rewards, gamma=0.9)

def test_value_iteration_convergence(sample_mdp):
    V, policy = sample_mdp.value_iteration()
    assert V[0] > V[1], "State 1 should have higher value"
    assert policy[0] == 0, "Optimal action in state 1 should be a1"

def test_treatment_path_generation():
    patient_data = {'vital_signs': {'bp_systolic': 185}}
    mdp = create_clinical_mdp(patient_data)
    path = mdp.generate_treatment_path('critical', horizon=3)
    assert len(path) == 3
    assert 'action' in path[0]
    assert 'probability' in path[0]

def test_patient_state_mapping():
    critical_patient = {'vital_signs': {'heart_rate': 130, 'bp_systolic': 190}}
    assert determine_initial_state(critical_patient) == 'critical'
    
    stable_patient = {'medical_history': {'chronic_conditions': ['diabetes']}}
    assert determine_initial_state(stable_patient) == 'stable'