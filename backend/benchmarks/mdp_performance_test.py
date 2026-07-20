import time
import pytest
import numpy as np
from services.mdp_engine import ClinicalMDP
from services.ddn_engine import ClinicalDDN

@pytest.fixture(params=['small', 'medium', 'large'])
def mdp_setup(request):
    scale = request.param
    if scale == 'small':
        states = [f's{i}' for i in range(10)]
        actions = [f'a{i}' for i in range(5)]
    elif scale == 'medium':
        states = [f's{i}' for i in range(100)]
        actions = [f'a{i}' for i in range(20)]
    else:
        states = [f's{i}' for i in range(1000)]
        actions = [f'a{i}' for i in range(50)]

    # Generate transition probabilities and rewards
    transition_probs = {
        s: {a: {s2: np.random.rand() for s2 in states} for a in actions}
        for s in states
    }
    rewards = {s: {a: np.random.rand() for a in actions} for s in states}
    
    return ClinicalMDP(states, actions, transition_probs, rewards)

@pytest.mark.benchmark(group="mdp_value_iteration")
def test_mdp_value_iteration(benchmark, mdp_setup):
    def run():
        return mdp_setup.value_iteration(epsilon=0.001)
    
    result = benchmark(run)
    assert len(result['policy']) == len(mdp_setup.states)

@pytest.fixture
def ddn_setup():
    states = ['healthy', 'critical', 'recovering']
    actions = ['monitor', 'intervene', 'discharge']
    observations = ['stable', 'unstable', 'critical']
    
    transition_model = {
        s: {a: {s2: np.random.dirichlet(np.ones(len(states))) for s2 in states} for a in actions}
        for s in states
    }
    
    observation_model = {
        s: {a: {o: np.random.dirichlet(np.ones(len(observations))) for o in observations} for a in actions}
        for s in states
    }
    
    reward_model = {s: {a: np.random.rand() for a in actions} for s in states}
    
    return ClinicalDDN(states, actions, observations, 
                      transition_model, observation_model, reward_model)

@pytest.mark.benchmark(group="ddn_belief_update")
def test_ddn_belief_update(benchmark, ddn_setup):
    belief = {'healthy': 0.6, 'critical': 0.3, 'recovering': 0.1}
    action = 'monitor'
    observation = 'stable'
    
    result = benchmark(ddn_setup.update_belief, belief, action, observation)
    assert abs(sum(result.probabilities.values()) - 1.0) < 1e-6