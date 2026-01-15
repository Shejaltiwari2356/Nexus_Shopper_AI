from pydantic import BaseModel, Field
from typing import List, Optional

class DecisionCriterion(BaseModel):
    name: str = Field(
        description="Human-level factor (e.g., Performance, Comfort, Durability)"
    )
    importance: float = Field(
        ge=0.0, le=1.0,
        description="How important this factor is to the user"
    )
    description: str = Field(
        description="Why this factor matters for this specific user"
    )

class UserIntent(BaseModel):
    product_category: Optional[str] = Field(
        description="Inferred or stated category (Laptop, Shoes, Camera, etc.)"
    )
    budget_limit: Optional[float] = Field(
        description="Maximum budget if mentioned by user"
    )
    criteria: List[DecisionCriterion]
