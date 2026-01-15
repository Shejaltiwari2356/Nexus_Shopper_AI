from schemas.intent import UserIntent
from core.llm import llm
from memory.vector_store import retrieve_preferences

SYSTEM_PROMPT = """
You are a professional shopping consultant.

Your task:
1. Analyze the user's request.
2. Consider their past preferences (if any) to refine the requirements.
3. Extract specific decision criteria.
4. Assign an importance score (0.0 to 1.0) for each criterion.
5. Infer the product category and identify a budget limit if mentioned.
"""

def extract_user_intent(user_query: str, user_id: str = "default") -> UserIntent:
    """
    Analyzes the query and past history to create a structured search intent.
    """
    # FIX: Pass user_query as the second argument for contextual preference retrieval
    past_prefs = retrieve_preferences(user_id, user_query)

    prompt = f"""
User request:
{user_query}

Context from User History:
{past_prefs}

Please convert this into a structured UserIntent.
"""

    structured_llm = llm.with_structured_output(UserIntent)
    return structured_llm.invoke(SYSTEM_PROMPT + prompt)