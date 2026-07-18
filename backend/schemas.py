from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class DDNSimulationParameters(BaseModel):
    horizon: int = 5
    discount_factor: float = 0.9
    max_iterations: int = 1000
    observation_model: Dict[str, Dict[str, Dict[str, float]]]
    initial_belief: Dict[str, float]

class BeliefState(BaseModel):
    probabilities: Dict[str, float]

class SimulationResult(BaseModel):
    optimal_path: List[dict]
    expected_utility: float
    belief_states: List[BeliefState]