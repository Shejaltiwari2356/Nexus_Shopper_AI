from pydantic import BaseModel, Field
from typing import List, Optional

class EvaluationFactor(BaseModel):
    criterion_name: str
    satisfied: bool
    score: float = Field(ge=0.0, le=1.0)
    reasoning: str

class ProductEvaluation(BaseModel):
    product_name: str
    overall_score: float = 0.0
    price: float
    platform: str
    factors: List[EvaluationFactor]
    risks: List[str]
    url: str
    
    # New fields for deep analysis
    summary_specs: str = Field(description="One-line technical summary")
    detailed_specs: str = Field(description="Full technical breakdown of the product")
    offer_analysis: str = Field(description="Comparison of price vs market value and platform reliability")
    debate_summary: Optional[str] = None