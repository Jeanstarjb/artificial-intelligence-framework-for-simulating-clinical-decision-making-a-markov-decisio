import pytest
from services.ddn_engine import ClinicalDDN, BeliefState

def test_belief_update():
    states = ['healthy', 'sepsis']
    actions = ['antibiotics', 'monitor']
    observations = ['normal', 'elevated']
    
    transition_model = {
        'healthy': {'antibiotics': {'healthy': 0.9, 'sepsis': 0.1},
                    'monitor': {'healthy': 0.7, 'sepsis': 0.3}},
        'sepsis': {'antibiotics': {'healthy': 0.4, 'sepsis': 0.6},
                   'monitor': {'healthy': 0.1, 'sepsis': 0.9}}
    }
    
    observation_model = {
        'healthy': {'antibiotics': {'normal': 0.8, 'elevated': 0.2},
                    'monitor': {'normal': 0.9, 'elevated': 0.1}},
        'sepsis': {'antibiotics': {'normal': 0.3, 'elevated': 0.7},
                   'monitor': {'normal': 0.1, 'elevated': 0.9}}
    }
    
    ddn = ClinicalDDN(states, actions, observations, transition_model, observation_model, {})
    
    prior_belief = BeliefState(probabilities={'healthy': 0.7, 'sepsis': 0.3})
    updated_belief = ddn.update_belief(prior_belief, 'antibiotics', 'elevated')
    
    assert sum(updated_belief.probabilities.values()) == pytest.approx(1.0)
    assert updated_belief.probabilities['sepsis'] > 0.3


def test_optimal_action_selection():
    ddn = ClinicalDDN([], [], [], {}, {}, {}, discount=0.9)
    belief = BeliefState(probabilities={'high_risk': 0.8, 'low_risk': 0.2})
    reward_model = {
        'high_risk': {'aggressive_treatment': 10, 'conservative': 5},
        'low_risk': {'aggressive_treatment': -2, 'conservative': 8}
    }
    optimal_action = ddn.select_action(belief, ['aggressive_treatment', 'conservative'], reward_model)
    
    expected_q_values = {
        'aggressive_treatment': 0.8*10 + 0.2*(-2),
        'conservative': 0.8*5 + 0.2*8
    }
    assert optimal_action == max(expected_q_values, key=expected_q_values.get)