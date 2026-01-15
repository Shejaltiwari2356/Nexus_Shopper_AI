import os
import requests
import re

class MarketplaceMCP:
    def __init__(self):
        self.api_key = os.getenv("SERPER_API_KEY")
        self.url = "https://google.serper.dev/shopping"

    def _clean_price(self, price_str: str) -> float:
        if not price_str: return 0.0
        match = re.search(r"(\d[\d,.]*)", str(price_str))
        if match:
            return float(match.group(1).replace(",", ""))
        return 0.0

    def search(self, query: str, budget: float | None = None):
        headers = {"X-API-KEY": self.api_key, "Content-Type": "application/json"}
        payload = {"q": query, "gl": "in", "hl": "en", "num": 20}

        response = requests.post(self.url, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        data = response.json()

        products = []
        for item in data.get("shopping", []):
            price = self._clean_price(item.get("price"))
            if budget and price > budget:
                continue

            products.append({
                "title": item.get("title"),
                "price": price,
                "platform": item.get("source"),
                "seller": item.get("seller"),
                "url": item.get("link"),
                "description": item.get("snippet", "")
            })
        return products