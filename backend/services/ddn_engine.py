from typing import Dict, List, Tuple
import numpy as np
from pydantic import BaseModel
from joblib import Parallel, delayed
from scipy.stats import entropy

class BeliefState(BaseModel):
    probabilities: Dict[str, float]

class ClinicalDDN:
    def __init__(self, states, actions, observations, transition_model, 
                 observation_model, reward_model, discount=0.9):
        self.states = states
        self.actions = actions
        self.observations = observations
        self.transition_model = transition_model
        self.observation_model = observation_model
        self.reward_model = reward_model
        self.discount = discount
        
        # Precompute matrices
        self.state_idx = {s: i for i, s in enumerate(states)}
        self.action_idx = {a: i for i, a in enumerate(actions)}
        self.obs_idx = {o: i for i, o in enumerate(observations)}
        
        self.T = np.zeros((len(states), len(actions), len(states)))
        self.O = np.zeros((len(states), len(actions), len(observations)))
        self.R = np.zeros((len(states), len(actions)))
        
        for s in states:
            s_i = self.state_idx[s]
            for a in actions:
                a_i = self.action_idx[a]
                self.R[s_i, a_i] = reward_model[s][a
                for s2 in transition_model[s][a]:
                    s2_i = self.state_idx[s2]
                    self.T[s_i, a_i, s2_i] = transition_model[s][a][s2]
                for o in observation_model[s][a]:
                    o_i = self.obs_idx[o]
                    self.O[s_i, a_i, o_i] = observation_model[s][a][o]

    def update_belief_vectorized(self, belief: np.ndarray, action: str, observation: str) -> np.ndarray:
        a_i = self.action_idx[action]
        o_i = self.obs_idx[observation]
        
        # Prediction step
        predicted_belief = np.dot(belief, self.T[:, a_i, :])
        
        # Update step
        likelihood = self.O[:, a_i, o_i]
        updated_belief = predicted_belief * likelihood
        updated_belief /= updated_belief.sum()
        
        return updated_belief

    def parallel_simulate_trajectories(self, initial_belief: Dict[str, float], 
                                      horizon: int, n_trajectories: int = 1000):
        initial_vec = np.array([initial_belief[s] for s in self.states])
        
        def simulate_trajectory(_):
            belief = initial_vec.copy()
            total_reward = 0
            
            for _ in range(horizon):
                action_probs = np.dot(belief, self.R + self.discount * np.einsum('ijk,k->ij', self.T, self.R))
                action_idx = np.argmax(action_probs)
                action = self.actions[action_idx]
                
                # Sample next state
                s_next = np.random.choice(len(self.states), p=self.T[:, action_idx, :].dot(belief))
                obs_probs = self.O[s_next, action_idx, :]
                observation = np.random.choice(len(self.observations), p=obs_probs)
                
                # Update belief
                belief = self.update_belief_vectorized(belief, action, self.observations[observation])
                total_reward += self.R[s_next, action_idx] * (self.discount ** _)
            
            return total_reward
        
        rewards = Parallel(n_jobs=-1)(
            delayed(simulate_trajectory)(i) for i in range(n_trajectories)
        )
        
        return np.mean(rewards), np.std(rewards)