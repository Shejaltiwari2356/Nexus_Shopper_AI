import os
import requests

class MarketplaceMCP:
    """
    MCP server for REAL ecommerce discovery using Serper (Google Shopping).
    """

    def __init__(self):
        self.api_key = os.getenv("SERPER_API_KEY")
        self.url = "https://google.serper.dev/shopping"

    def search(self, query: str, budget: float | None = None):
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "q": query,
            "gl": "in",
            "hl": "en"
        }

        response = requests.post(
            self.url,
            headers=headers,
            json=payload,
            timeout=20
        )

        response.raise_for_status()
        data = response.json()

        products = []

        for item in data.get("shopping", []):
            price = item.get("price")

            if price:
                price = float(
                    price.replace("₹", "").replace(",", "")
                )

            if budget and price and price > budget:
                continue

            products.append({
                "title": item.get("title"),
                "price": price,
                "platform": item.get("source"),
                "seller": item.get("seller"),
                "availability": True,
                "url": item.get("link")
            })

        return products
