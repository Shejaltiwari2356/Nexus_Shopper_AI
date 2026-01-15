from pydantic import BaseModel
from typing import List

class Recommendation(BaseModel):
    best_choice: str
    justification: str
    alternatives: List[str]
    confidence: float
