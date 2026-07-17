import numpy as np
from scipy.optimize import linear_sum_assignment
from typing import Dict, List, Tuple

class ClinicalMDP:
    def __init__(self, states: List[str], actions: List[str], transition_probs: Dict[str, Dict[str, Dict[str, float]]], rewards: Dict[str, Dict[str, float]], gamma: float = 0.9):
        self.states = states
        self.actions = actions
        self.transition_probs = transition_probs
        self.rewards = rewards
        self.gamma = gamma
        self.n_states = len(states)
        self.n_actions = len(actions)
        self.state_to_idx = {s: i for i, s in enumerate(states)}
        self.action_to_idx = {a: i for i, a in enumerate(actions)}

    def value_iteration(self, max_iterations: int = 1000, tol: float = 1e-6) -> Tuple[np.ndarray, np.ndarray]:
        V = np.zeros(self.n_states)
        policy = np.zeros(self.n_states, dtype=int)

        for _ in range(max_iterations):
            V_prev = np.copy(V)
            for s_idx, s in enumerate(self.states):
                q_values = np.zeros(self.n_actions)
                for a_idx, a in enumerate(self.actions):
                    for next_s, prob in self.transition_probs.get(s, {}).get(a, {}).items():
                        next_s_idx = self.state_to_idx[next_s]
                        q_values[a_idx] += prob * (self.rewards.get(s, {}).get(a, 0) + self.gamma * V_prev[next_s_idx])
                if len(q_values) > 0:
                    V[s_idx] = np.max(q_values)
                    policy[s_idx] = np.argmax(q_values)
            if np.max(np.abs(V - V_prev)) < tol:
                break
        return V, policy

    def get_optimal_policy(self, max_iterations: int = 1000) -> Dict[str, str]:
        _, policy = self.value_iteration(max_iterations)
        return {s: self.actions[policy[i]] for i, s in enumerate(self.states)}

    def generate_treatment_path(self, initial_state: str, horizon: int = 5) -> List[Dict]:
        path = []
        current_state = initial_state
        policy = self.get_optimal_policy()

        for _ in range(horizon):
            if current_state not in self.states:
                break
            action = policy[current_state]
            transitions = self.transition_probs.get(current_state, {}).get(action, {})
            next_states = list(transitions.keys())
            probs = list(transitions.values())
            next_state = np.random.choice(next_states, p=probs) if next_states else current_state
            
            path.append({
                "state": current_state,
                "action": action,
                "probability": transitions.get(next_state, 0.0),
                "reward": self.rewards.get(current_state, {}).get(action, 0.0)
            })
            current_state = next_state
        return path


def create_clinical_mdp(patient_data: Dict) -> ClinicalMDP:
    states = ["critical", "stable", "improving", "recovered"]
    actions = ["aggressive_treatment", "conservative", "monitor", "rehab"]
    
    transition_probs = {
        "critical": {
            "aggressive_treatment": {"stable": 0.6, "critical": 0.4},
            "conservative": {"stable": 0.3, "critical": 0.7}
        },
        "stable": {
            "conservative": {"improving": 0.5, "stable": 0.5},
            "rehab": {"improving": 0.7, "stable": 0.3}
        },
        "improving": {
            "rehab": {"recovered": 0.8, "improving": 0.2},
            "monitor": {"recovered": 0.5, "improving": 0.5}
        },
        "recovered": {"monitor": {"recovered": 1.0}}
    }

    rewards = {
        "critical": {"aggressive_treatment": -1.0, "conservative": -0.5},
        "stable": {"conservative": 0.0, "rehab": 0.3},
        "improving": {"rehab": 0.8, "monitor": 0.5},
        "recovered": {"monitor": 1.0}
    }

    if patient_data.get('vital_signs', {}).get('bp_systolic', 0) > 180:
        transition_probs["critical"]["aggressive_treatment"]["stable"] = 0.4
        transition_probs["critical"]["aggressive_treatment"]["critical"] = 0.6

    return ClinicalMDP(states, actions, transition_probs, rewards)