from typing import Dict
from schemas.intent import UserIntent
from schemas.evaluation import ProductEvaluation
from core.llm import llm
from tools.aggregation import aggregate_score
from crews.evaluation_crew import debate_evaluation

SYSTEM_PROMPT = """
You are a Technical Specification Expert and Deal Analyst.

Your task:
1. Extract ALL technical specifications from the product description.
2. Evaluate 'Offer Value' by comparing price and platform reliability.
3. Judge satisfaction for each user criterion and assign a score (0 to 1).
4. Provide a 1-line summary and a full technical breakdown.
"""

def evaluate_product(intent: UserIntent, product: Dict) -> ProductEvaluation:
    structured_llm = llm.with_structured_output(ProductEvaluation)
    prompt = f"User Intent:\n{intent}\n\nProduct Info:\n{product}\n\nEvaluate in detail."
    
    evaluation = structured_llm.invoke(SYSTEM_PROMPT + prompt)
    evaluation.overall_score = aggregate_score(evaluation, intent)
    evaluation.debate_summary = debate_evaluation(evaluation)
    
    return evaluation