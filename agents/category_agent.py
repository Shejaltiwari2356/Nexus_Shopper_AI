from core.llm import llm

SYSTEM_PROMPT = """
You are a product categorization expert.

Your task:
- Infer the most likely ecommerce product category
- Be concise
- Output a single category name only

Examples:
- Laptop
- Smartphone
- Headphones
- Shoes
- Furniture
- Course
"""

def infer_category(user_query: str) -> str:
    response = llm.invoke(
        SYSTEM_PROMPT + f"\nUser request:\n{user_query}"
    )
    return response.content.strip()
