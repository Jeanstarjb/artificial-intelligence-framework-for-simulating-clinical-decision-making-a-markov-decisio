import pytest
from services.mdp_engine import ClinicalMDP
import numpy as np

def test_value_iteration():
    states = ['s0', 's1']
    actions = ['a0', 'a1']
    transition_probs = {
        's0': {'a0': {'s0': 0.5, 's1': 0.5}, 'a1': {'s0': 0.1, 's1': 0.9}},
        's1': {'a0': {'s0': 0.8, 's1': 0.2}, 'a1': {'s0': 0.0, 's1': 1.0}}
    }
    rewards = {'s0': {'a0': 5, 'a1': 10}, 's1': {'a0': -1, 'a1': 2}}
    mdp = ClinicalMDP(states, actions, transition_probs, rewards)
    optimal_values, policy = mdp.value_iteration(0.001)
    
    assert len(optimal_values) == 2
    assert policy['s0'] in actions
    assert np.allclose(optimal_values['s1'], 2/(1-0.9), rtol=0.1)


def test_policy_extraction():
    states = ['s0', 's1']
    actions = ['a0', 'a1']
    transition_probs = {
        's0': {'a0': {'s0': 1.0}, 'a1': {'s1': 1.0}},
        's1': {'a0': {'s0': 1.0}, 'a1': {'s1': 1.0}}
    }
    rewards = {'s0': {'a0': 1, 'a1': 0}, 's1': {'a0': 0, 'a1': 2}}
    mdp = ClinicalMDP(states, actions, transition_probs, rewards, gamma=0.9)
    values, policy = mdp.value_iteration()
    
    assert policy['s0'] == 'a0'
    assert policy['s1'] == 'a1'