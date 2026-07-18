import pytest
from services.policy_evaluator import PolicyEvaluator
from services.mdp_engine import ClinicalMDP
from services.ddn_engine import ClinicalDDN, BeliefState

@pytest.fixture
def sample_mdp():
    states = ['s1', 's2']
    actions = ['a1', 'a2']
    transition_probs = {
        's1': {'a1': {'s2': 1.0}, 'a2': {'s1': 1.0}},
        's2': {'a1': {'s2': 1.0}, 'a2': {'s1': 1.0}}
    }
    rewards = {'s1': {'a1': 5.0, 'a2': 0}, 's2': {'a1': -1.0, 'a2': 0}}
    return ClinicalMDP(states, actions, transition_probs, rewards)

@pytest.fixture
def sample_ddn():
    return ClinicalDDN(
        states=['stable', 'critical'],
        actions=['monitor', 'intervene'],
        observations=['normal', 'abnormal'],
        transition_model={
            'stable': {
                'monitor': {'stable': 0.8, 'critical': 0.2},
                'intervene': {'stable': 0.9, 'critical': 0.1}
            },
            'critical': {
                'monitor': {'stable': 0.3, 'critical': 0.7},
                'intervene': {'stable': 0.6, 'critical': 0.4}
            }
        },
        observation_model={
            'stable': {
                'monitor': {'normal': 0.9, 'abnormal': 0.1},
                'intervene': {'normal': 0.7, 'abnormal': 0.3}
            },
            'critical': {
                'monitor': {'normal': 0.2, 'abnormal': 0.8},
                'intervene': {'normal': 0.5, 'abnormal': 0.5}
            }
        },
        reward_model={
            'stable': {'monitor': 1.0, 'intervene': 0.8},
            'critical': {'monitor': -2.0, 'intervene': -1.0}
        }
    )

def test_mdp_policy_evaluation(sample_mdp, sample_ddn):
    evaluator = PolicyEvaluator(sample_mdp, sample_ddn)
    policy = {'s1': 'a1', 's2': 'a2'}
    results = evaluator.evaluate_mdp_policy(policy, n_simulations=100)
    assert 'mean_reward' in results
    assert results['mean_reward'] > 0

def test_ddn_belief_update(sample_ddn):
    initial_belief = BeliefState(probabilities={'stable': 0.7, 'critical': 0.3})
    updated_belief = sample_ddn.update_belief(initial_belief, 'monitor', 'normal')
    assert sum(updated_belief.probabilities.values()) == pytest.approx(1.0)

def test_monte_carlo_simulation(sample_ddn):
    belief = BeliefState(probabilities={'stable': 0.6, 'critical': 0.4})
    results = sample_ddn.monte_carlo_simulate_path(belief, {'type': 'clinical_guidelines'})
    assert len(results['state_history']) == 100
    assert 'total_discounted_reward' in results
