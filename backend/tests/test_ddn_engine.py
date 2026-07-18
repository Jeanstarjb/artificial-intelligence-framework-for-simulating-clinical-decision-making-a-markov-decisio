import pytest
from services.ddn_engine import ClinicalDDN, BeliefState

@pytest.fixture
def sample_ddn() -> ClinicalDDN:
    states = ['stable', 'critical']
    actions = ['monitor', 'intervene']
    observations = ['normal_readings', 'abnormal_readings']
    
    transition_model = {
        'stable': {
            'monitor': {'stable': 0.8, 'critical': 0.2},
            'intervene': {'stable': 0.9, 'critical': 0.1}
        },
        'critical': {
            'monitor': {'stable': 0.3, 'critical': 0.7},
            'intervene': {'stable': 0.6, 'critical': 0.4}
        }
    }
    
    observation_model = {
        'stable': {
            'monitor': {'normal_readings': 0.9, 'abnormal_readings': 0.1},
            'intervene': {'normal_readings': 0.7, 'abnormal_readings': 0.3}
        },
        'critical': {
            'monitor': {'normal_readings': 0.2, 'abnormal_readings': 0.8},
            'intervene': {'normal_readings': 0.4, 'abnormal_readings': 0.6}
        }
    }
    
    reward_model = {
        'stable': {'monitor': 5, 'intervene': 3},
        'critical': {'monitor': -10, 'intervene': -5}
    }
    
    return ClinicalDDN(states, actions, observations,
                      transition_model, observation_model,
                      reward_model, discount=0.9)

def test_belief_update(sample_ddn):
    initial_belief = BeliefState(probabilities={'stable': 0.7, 'critical': 0.3})
    updated_belief = sample_ddn.update_belief(
        initial_belief,
        action='monitor',
        observation='normal_readings'
    )
    
    assert sum(updated_belief.probabilities.values()) == pytest.approx(1.0)
    assert updated_belief.probabilities['stable'] > 0.7  # Should increase with normal reading

def test_policy_generation(sample_ddn):
    initial_belief = BeliefState(probabilities={'stable': 0.5, 'critical': 0.5})
    value, policy = sample_ddn.value_iteration(initial_belief, horizon=3)
    
    assert len(policy) == 3
    assert 'stable' in policy[0]
    assert policy[0]['stable'] in ['monitor', 'intervene']
    
    # Verify policy improves expected value
    assert value > -5  # Worst case scenario baseline