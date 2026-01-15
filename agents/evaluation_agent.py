from typing import Dict
from schemas.intent import UserIntent
from schemas.evaluation import ProductEvaluation
from core.llm import llm
from tools.aggregation import aggregate_score
from crews.evaluation_crew import debate_evaluation

SYSTEM_PROMPT = """
You are an expert evaluator.

Your task:
- Evaluate a product against user decision criteria
- Judge satisfaction for each criterion
- Assign a score between 0 and 1
- Provide clear reasoning
"""

def evaluate_product(
    intent: UserIntent,
    product: Dict
) -> ProductEvaluation:
    """
    Evaluate a single product using LLM reasoning,
    then apply deterministic scoring and crew debate.
    """

    structured_llm = llm.with_structured_output(ProductEvaluation)

    prompt = f"""
User Intent:
{intent}

Product Info:
{product}

Evaluate this product.
"""

    # 🧠 LLM-based evaluation
    evaluation = structured_llm.invoke(SYSTEM_PROMPT + prompt)

    # 🔥 Deterministic aggregation (Phase 3)
    evaluation.overall_score = aggregate_score(evaluation, intent)

    # 🤝 Crew-based debate (Phase 3)
    evaluation.debate_summary = debate_evaluation(evaluation)

    return evaluation
