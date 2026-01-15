from typing import Dict
from pydantic import BaseModel, Field
from schemas.intent import UserIntent
from core.llm import llm

class EligibilityResult(BaseModel):
    is_eligible: bool = Field(description="Whether the product matches the user's core requirements")
    reason: str = Field(description="Brief reason for eligibility or rejection")

def is_eligible(intent: UserIntent, product: Dict) -> bool:
    """
    Intelligent gatekeeper using LLM reasoning to filter products.
    """
    # 1. Hard Budget Constraint (Deterministic)
    if intent.budget_limit:
        price = extract_price(product)
        if price and price > intent.budget_limit:
            return False

    # 2. LLM-based Qualitative Filtering
    structured_llm = llm.with_structured_output(EligibilityResult)
    
    prompt = f"""
    You are a product gatekeeper. Determine if this product is a serious candidate 
    based on the user's intent. 
    
    User Intent:
    - Category: {intent.product_category}
    - Criteria: {[c.name for c in intent.criteria]}
    
    Product to Check:
    - Title: {product.get('title')}
    - Description: {product.get('description')}
    
    A product is eligible if it matches the category and has a reasonable chance 
    of satisfying at least some of the user's criteria. Be inclusive but reject 
    completely irrelevant items.
    """
    
    try:
        result = structured_llm.invoke(prompt)
        return result.is_eligible
    except Exception:
        # Fallback to True if LLM fails to avoid losing potential results
        return True

def extract_price(product: dict):
    """
    Safe price extraction across ecommerce sources.
    """
    raw_price = product.get("price")
    if not raw_price:
        return None

    try:
        return float(
            str(raw_price)
            .replace(",", "")
            .replace("₹", "")
            .replace("$", "")
        )
    except Exception:
        return None