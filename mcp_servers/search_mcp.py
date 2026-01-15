import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

class SearchMCPServer:
    """
    MCP Server for web/product search.
    This isolates external tools from agents.
    """

    def search(self, query: str, max_results: int = 5):
        response = client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced",
            include_answer=False,
            include_raw_content=False,
        )

        return [
            {
                "name": r.get("title"),
                "description": r.get("content"),
                "url": r.get("url"),
            }
            for r in response.get("results", [])
        ]
