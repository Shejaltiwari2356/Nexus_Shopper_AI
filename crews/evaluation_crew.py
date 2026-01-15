from core.llm import llm
from schemas.evaluation import ProductEvaluation

SYSTEM_PROMPTS = {
    "optimist": "Focus on strengths and best possible interpretation.",
    "skeptic": "Focus on weaknesses, risks, and missing information.",
    "judge": "Balance both sides and give a final verdict."
}

def debate_evaluation(evaluation: ProductEvaluation) -> str:
    debate = ""

    for role, prompt in SYSTEM_PROMPTS.items():
        response = llm.invoke(
            f"""
Role: {role}
Instruction: {prompt}

Product Evaluation:
{evaluation}

Give your opinion in 2-3 lines.
"""
        )
        debate += f"\n[{role.upper()}]\n{response.content}\n"

    return debate
