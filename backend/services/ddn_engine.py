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

    def update_belief(self, belief: BeliefState, action: str, observation: str) -> BeliefState:
        """Bayesian belief update using observation model"""
        new_belief = {}
        total = 0.0
        for state in self.states:
            prob = 0.0
            for prev_state in self.states:
                prob += (
                    self.transition_model[prev_state][action][state] *
                    self.observation_model[state][action][observation] *
                    belief.probabilities[prev_state]
                )
            new_belief[state] = prob
            total += prob
        
        # Normalize probabilities
        return BeliefState(probabilities={s: p/total for s, p in new_belief.items()})

    def monte_carlo_simulate_path(self, initial_belief: BeliefState, policy: Dict, steps: int = 100) -> Dict:
        """Simulate treatment path with probabilistic outcomes"""
        current_belief = initial_belief
        history = []
        total_reward = 0.0

        for t in range(steps):
            # Get action from policy based on current belief
            action = self._select_action_from_policy(current_belief, policy)
            
            # Sample next state from transition model
            true_state = np.random.choice(
                self.states,
                p=[current_belief.probabilities[s] for s in self.states]
            )
            next_state_probs = self.transition_model[true_state][action]
            next_state = np.random.choice(list(next_state_probs.keys()), p=list(next_state_probs.values()))
            
            # Get observation
            observation_probs = self.observation_model[next_state][action]
            observation = np.random.choice(list(observation_probs.keys()), p=list(observation_probs.values()))
            
            # Update belief and accumulate reward
            current_belief = self.update_belief(current_belief, action, observation)
            reward = self.reward_model[true_state][action]
            total_reward += (self.discount ** t) * reward
            
            history.append({
                'step': t,
                'action': action,
                'true_state': true_state,
                'observed': observation,
                'belief': current_belief.dict(),
                'immediate_reward': reward
            })

        return {
            'total_discounted_reward': total_reward,
            'final_belief': current_belief.dict(),
            'state_history': history,
            'qaly_equivalent': total_reward * 0.85  # Example conversion factor
        }

    def _select_action_from_policy(self, belief: BeliefState, policy: Dict) -> str:
        """Select action based on policy type"""
        if policy['type'] == 'optimal':
            return self._optimal_action(belief)
        elif policy['type'] == 'random':
            return np.random.choice(self.actions)
        elif policy['type'] == 'clinical_guidelines':
            return self._guideline_based_action(belief)
        else:
            raise ValueError("Unknown policy type")

    def _optimal_action(self, belief: BeliefState) -> str:
        """Calculate optimal action using value iteration"""
        # Implementation of value iteration for POMDP
        # [This would be expanded with actual algorithm]
        return self.actions[0]

    def _guideline_based_action(self, belief: BeliefState) -> str:
        """Heuristic based on clinical guidelines"""
        most_likely_state = max(belief.probabilities, key=belief.probabilities.get)
        return 'monitor' if most_likely_state == 'stable' else 'intervene'
