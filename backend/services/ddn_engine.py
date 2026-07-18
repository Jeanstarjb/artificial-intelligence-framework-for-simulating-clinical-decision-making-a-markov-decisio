from typing import Dict, List, Tuple
import numpy as np
from scipy.stats import entropy
from pydantic import BaseModel

class BeliefState(BaseModel):
    probabilities: Dict[str, float]

class ClinicalDDN:
    def __init__(self,
                 states: List[str],
                 actions: List[str],
                 observations: List[str],
                 transition_model: Dict[str, Dict[str, Dict[str, float]]],
                 observation_model: Dict[str, Dict[str, Dict[str, float]]],
                 reward_model: Dict[str, Dict[str, float]],
                 discount: float = 0.9):
        self.states = states
        self.actions = actions
        self.observations = observations
        self.transition_model = transition_model
        self.observation_model = observation_model
        self.reward_model = reward_model
        self.discount = discount
        self.state_idx = {s: i for i, s in enumerate(states)}
        self.action_idx = {a: i for i, a in enumerate(actions)}
        self.obs_idx = {o: i for i, o in enumerate(observations)}

    def update_belief(self,
                     belief: BeliefState,
                     action: str,
                     observation: str) -> BeliefState:
        new_belief = {}
        for s_prime in self.states:
            total = 0.0
            for s in self.states:
                trans_prob = self.transition_model[s].get(action, {}).get(s_prime, 0.0)
                obs_prob = self.observation_model[s_prime].get(action, {}).get(observation, 0.0)
                total += belief.probabilities.get(s, 0.0) * trans_prob * obs_prob
            new_belief[s_prime] = total
        
        # Normalize
        total_prob = sum(new_belief.values())
        return BeliefState(probabilities={s: prob/total_prob for s, prob in new_belief.items()})

    def value_iteration(self,
                       initial_belief: BeliefState,
                       horizon: int = 5) -> Tuple[Dict[str, float], Dict[str, str]]:
        V = [{} for _ in range(horizon+1)]
        policy = [{} for _ in range(horizon)]
        
        # Initialize terminal values
        for s in self.states:
            V[horizon][s] = 0.0
        
        for t in reversed(range(horizon)):
            for s in self.states:
                max_value = -np.inf
                best_action = None
                for a in self.actions:
                    exp_reward = 0.0
                    for s_prime in self.states:
                        trans_prob = self.transition_model[s].get(a, {}).get(s_prime, 0.0)
                        reward = self.reward_model[s].get(a, 0.0)
                        obs_prob = sum(
                            self.observation_model[s_prime].get(a, {}).get(o, 0.0)
                            for o in self.observations
                        )
                        exp_reward += trans_prob * (reward + self.discount * V[t+1][s_prime] * obs_prob)
                    if exp_reward > max_value:
                        max_value = exp_reward
                        best_action = a
                V[t][s] = max_value
                policy[t][s] = best_action
        
        # Calculate initial value based on belief
        initial_value = sum(initial_belief.probabilities[s] * V[0][s] for s in self.states)
        return initial_value, policy

    def generate_optimal_path(self,
                             initial_belief: BeliefState,
                             horizon: int) -> List[Dict]:
        path = []
        current_belief = initial_belief
        _, policy = self.value_iteration(initial_belief, horizon)
        
        for t in range(horizon):
            if not policy[t]:
                break
            
            # Choose action based on maximum expected reward
            action = max(policy[t], key=lambda s: current_belief.probabilities.get(s, 0))
            
            # Simulate transition and observation (would be real data in production)
            # For simulation purposes, sample next state and observation
            next_state = np.random.choice(
                self.states,
                p=[current_belief.probabilities[s] for s in self.states]
            )
            observation = np.random.choice(
                self.observations,
                p=list(self.observation_model[next_state][action].values())
            )
            
            path.append({
                'belief_state': current_belief.dict(),
                'action': action,
                'observation': observation,
                'reward': self.reward_model[next_state][action]
            })
            
            current_belief = self.update_belief(current_belief, action, observation)
        
        return path