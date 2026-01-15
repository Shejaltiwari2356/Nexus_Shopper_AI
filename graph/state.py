from typing import List, Dict, Optional, Annotated
import operator
from schemas.intent import UserIntent
from schemas.evaluation import ProductEvaluation
from schemas.recommendation import Recommendation

class ShopperState(dict):
    """
    Shared state across LangGraph nodes.
    Uses Annotated to ensure lists are merged, not overwritten.
    """
    user_query: str
    intent: Optional[UserIntent] = None
    
    # Ensures new products/evaluations are added to existing ones
    products: Annotated[List[Dict], operator.add] = []
    evaluations: Annotated[List[ProductEvaluation], operator.add] = []
    
    recommendation: Optional[Recommendation] = None
    decision: Optional[str] = None