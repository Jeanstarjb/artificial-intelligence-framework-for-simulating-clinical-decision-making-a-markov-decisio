from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

# Existing schemas...

class PolicyEvaluationResult(BaseModel):
    optimal_actions: Dict[str, str]
    value_function: Dict[str, float]
    convergence_iterations: int
    qaly_estimate: float
    cost_effectiveness: Dict[str, float]
    sensitivity_ranges: Dict[str, List[float]]

class MonteCarloResult(BaseModel):
    simulation_id: str
    total_reward: float
    qaly_equivalent: float
    state_history: List[Dict]
    confidence_interval: List[float]
    class Config:
        json_encoders = {
            np.ndarray: lambda v: v.tolist(),
        }

class ComparativePolicyAnalysis(BaseModel):
    policies: List[str]
    qaly_comparison: Dict[str, float]
    cost_comparison: Dict[str, float]
    dominance_analysis: Dict[str, bool]
    probabilistic_sensitivity: Dict[str, List[float]]

class DDNSimulationParameters(BaseModel):
    simulation_type: str = Field(..., regex="^(mdp|ddn)$")
    horizon_steps: int = Field(10, ge=1, le=100)
    monte_carlo_runs: int = Field(1000, ge=100, le=10000)
    policy_constraints: Optional[Dict[str, List[str]]]
    reward_weights: Dict[str, float]
    discount_factor: float = Field(0.9, ge=0.8, le=0.99)
    sensitivity_params: Optional[List[str]]

class SimulationResult(BaseModel):
    optimal_policy: Dict
    value_estimates: Dict
    probabilistic_outcomes: Dict
    sensitivity_analysis: Dict
    clinical_metrics: Dict
    simulation_metadata: Dict
