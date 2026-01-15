from schemas.intent import UserIntent
from mcp_servers.marketplace_mcp import MarketplaceMCP

marketplace = MarketplaceMCP()

def discover_options(intent: UserIntent):
    """
    Discover REAL purchasable products from ecommerce platforms.
    """
    query = intent.product_category

    return marketplace.search(
        query=query,
        budget=intent.budget_limit
    )
