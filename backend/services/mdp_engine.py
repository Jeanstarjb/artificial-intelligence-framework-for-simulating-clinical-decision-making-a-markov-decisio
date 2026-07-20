import numpy as np
from scipy.optimize import linear_sum_assignment
from typing import Dict, List, Tuple
from heapq import heappush, heappop

class ClinicalMDP:
    def __init__(self, states: List[str], actions: List[str], 
                 transition_probs: Dict[str, Dict[str, Dict[str, float]]], 
                 rewards: Dict[str, Dict[str, float]], gamma: float = 0.9):
        self.states = states
        self.actions = actions
        self.transition_probs = transition_probs
        self.rewards = rewards
        self.gamma = gamma
        self.state_idx = {s: i for i, s in enumerate(states)}
        self.action_idx = {a: i for i, a in enumerate(actions)}
        self.n_states = len(states)
        self.n_actions = len(actions)
        
        # Precompute transition matrices
        self.T = np.zeros((self.n_states, self.n_actions, self.n_states))
        self.R = np.zeros((self.n_states, self.n_actions))
        
        for s_idx, s in enumerate(states):
            for a_idx, a in enumerate(actions):
                self.R[s_idx, a_idx] = rewards[s].get(a, 0)
                for s2 in transition_probs[s][a]:
                    self.T[s_idx, a_idx, self.state_idx[s2]] = transition_probs[s][a][s2]

    def value_iteration(self, epsilon=1e-6, max_iter=1000):
        V = np.zeros(self.n_states)
        policy = np.zeros(self.n_states, dtype=int)
        
        for _ in range(max_iter):
            V_prev = V.copy()
            Q = self.R + self.gamma * np.einsum('ijk,k->ij', self.T, V)
            V = np.max(Q, axis=1)
            policy = np.argmax(Q, axis=1)
            
            if np.max(np.abs(V - V_prev)) < epsilon:
                break
        
        return {
            'values': {s: V[i] for i, s in enumerate(self.states)},
            'policy': {s: self.actions[policy[i]] for i, s in enumerate(self.states)}
        }

    def prioritized_sweeping_value_iteration(self, epsilon=1e-6, max_iter=1000):
        V = np.zeros(self.n_states)
        policy = np.zeros(self.n_states, dtype=int)
        priority_queue = []
        
        # Initialize priorities
        for s_idx in range(self.n_states):
            heappush(priority_queue, (-np.inf, s_idx))
        
        for _ in range(max_iter):
            if not priority_queue:
                break
            
            _, s_idx = heappop(priority_queue)
            old_value = V[s_idx]
            
            Q = self.R[s_idx] + self.gamma * np.dot(self.T[s_idx], V)
            V[s_idx] = np.max(Q)
            policy[s_idx] = np.argmax(Q)
            
            delta = abs(old_value - V[s_idx])
            
            # Update predecessors' priorities
            for a_idx in range(self.n_actions):
                for pred_idx in np.where(self.T[:, a_idx, s_idx] > 0)[0]:
                    Q_pred = self.R[pred_idx] + self.gamma * np.dot(self.T[pred_idx], V)
                    best_q = np.max(Q_pred)
                    priority = -abs(V[pred_idx] - best_q)
                    heappush(priority_queue, (priority, pred_idx))
            
            if delta < epsilon:
                break
        
        return {
            'values': {s: V[i] for i, s in enumerate(self.states)},
            'policy': {s: self.actions[policy[i]] for i, s in enumerate(self.states)}
        }