from schemas.intent import UserIntent

def explain_no_match(intent: UserIntent) -> str:
    reasons = []
    suggestions = []

    if intent.budget_limit:
        reasons.append(
            f"Budget of ₹{int(intent.budget_limit)} is too restrictive."
        )
        suggestions.append(
            "Increase budget or consider refurbished options."
        )

    for c in intent.criteria:
        desc = c.description.lower()

        if "machine learning" in desc or "ml" in desc:
            reasons.append(
                "Machine learning requires high-end CPU and dedicated GPU."
            )
            suggestions.append(
                "Use cloud ML platforms like Google Colab or AWS."
            )

        if "portable" in desc or "lightweight" in desc:
            reasons.append(
                "High performance conflicts with portability."
            )
            suggestions.append(
                "Relax portability or accept a heavier device."
            )

    return (
        "⚠️ No products matched all your requirements.\n\n"
        "Why:\n- " + "\n- ".join(reasons) +
        "\n\nWhat you can do:\n- " + "\n- ".join(set(suggestions))
    )
