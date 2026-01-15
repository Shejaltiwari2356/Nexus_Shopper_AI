from schemas.intent import UserIntent

def is_eligible(intent: UserIntent, product: dict) -> bool:
    """
    Category-agnostic eligibility filter.
    Works for ANY product type.
    """

    # 1️⃣ Must be a real purchasable product
    required_fields = ["title", "url"]
    if not all(product.get(f) for f in required_fields):
        return False

    # 2️⃣ Budget is a HARD constraint (if provided)
    if intent.budget_limit:
        price = extract_price(product)
        if price is None or price > intent.budget_limit:
            return False

    # 3️⃣ Must contain signals related to decision criteria
    searchable_text = (
        product.get("title", "") + " " +
        product.get("description", "")
    ).lower()

    signal_hits = 0
    for criterion in intent.criteria:
        if criterion.name.lower() in searchable_text:
            signal_hits += 1

    # At least ONE criterion must be evaluable
    return signal_hits > 0


def extract_price(product: dict):
    """
    Safe price extraction across ecommerce sources
    """
    raw_price = product.get("price")
    if not raw_price:
        return None

    try:
        return float(
            str(raw_price)
            .replace(",", "")
            .replace("₹", "")
            .replace("$", "")
        )
    except:
        return None
