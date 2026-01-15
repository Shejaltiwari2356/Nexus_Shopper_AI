import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_products(query: str, max_results: int = 5):
    """
    Generic product discovery via web search.
    Product-agnostic.
    """
    response = client.search(
        query=query,
        max_results=max_results,
        search_depth="advanced",
        include_answer=False,
        include_raw_content=False,
    )

    results = []
    for r in response.get("results", []):
        results.append({
            "name": r.get("title"),
            "description": r.get("content"),
            "url": r.get("url"),
        })

    return results
