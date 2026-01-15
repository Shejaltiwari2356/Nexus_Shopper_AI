from schemas.intent import UserIntent
from core.llm import llm
from memory.vector_store import retrieve_preferences

SYSTEM_PROMPT = """
You are a professional shopping consultant.

You must:
- Consider the user's past preferences if provided
- Extract decision criteria
- Assign importance between 0 and 1
"""

def extract_user_intent(user_query: str, user_id: str = "default") -> UserIntent:
    past_prefs = retrieve_preferences(user_id)

    prompt = f"""
User request:
{user_query}

Past preferences:
{past_prefs}
"""

    structured_llm = llm.with_structured_output(UserIntent)
    return structured_llm.invoke(SYSTEM_PROMPT + prompt)
