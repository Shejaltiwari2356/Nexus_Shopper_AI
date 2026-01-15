from typing import List, Dict, Optional
from schemas.intent import UserIntent
from schemas.evaluation import ProductEvaluation

class ShopperState(dict):
    """
    Shared state across LangGraph nodes.
    """

    user_query: str

    intent: Optional[UserIntent] = None

    products: Optional[List[Dict]] = None

    evaluations: Optional[List[ProductEvaluation]] = None

    # ✅ THIS WAS MISSING
    decision: Optional[str] = None
