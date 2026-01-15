from typing import List
from schemas.evaluation import ProductEvaluation
from schemas.recommendation import Recommendation
from core.llm import llm

SYSTEM_PROMPT = """
You are a decision assistant.

Your task:
- Compare product evaluations
- Pick the best option
- Suggest alternatives
- Explain reasoning clearly
"""

def recommend(evaluations: List[ProductEvaluation]) -> Recommendation:
    structured_llm = llm.with_structured_output(Recommendation)

    prompt = f"""
Product evaluations:
{evaluations}

Make a final recommendation.
"""

    return structured_llm.invoke(SYSTEM_PROMPT + prompt)
