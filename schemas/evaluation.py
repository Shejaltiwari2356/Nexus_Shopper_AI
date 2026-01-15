from pydantic import BaseModel, Field
from typing import List, Optional

class EvaluationFactor(BaseModel):
    criterion_name: str
    satisfied: bool
    score: float = Field(ge=0.0, le=1.0)
    reasoning: str

class ProductEvaluation(BaseModel):
    product_name: str
    overall_score: float
    factors: List[EvaluationFactor]
    risks: List[str]
    url: str

    # ✅ NEW (Phase 3)
    debate_summary: Optional[str] = None
