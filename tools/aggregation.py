from schemas.evaluation import ProductEvaluation
from schemas.intent import UserIntent

def aggregate_score(
    evaluation: ProductEvaluation,
    intent: UserIntent
) -> float:
    """
    Deterministic, normalized scoring:
    - Weighted average by importance
    - Penalize risks
    - Final score in range [0, 1]
    """

    importance_map = {
        c.name: c.importance for c in intent.criteria
    }

    weighted_sum = 0.0
    total_importance = 0.0

    for factor in evaluation.factors:
        importance = importance_map.get(factor.criterion_name, 0.0)
        weighted_sum += factor.score * importance
        total_importance += importance

    if total_importance == 0:
        base_score = 0.0
    else:
        base_score = weighted_sum / total_importance  # 🔑 NORMALIZATION

    # Risk penalty
    risk_penalty = 0.05 * len(evaluation.risks)

    final_score = base_score - risk_penalty

    return round(max(final_score, 0.0), 3)
