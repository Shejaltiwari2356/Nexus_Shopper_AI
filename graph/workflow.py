from langgraph.graph import StateGraph
from graph.state import ShopperState

from agents.consultant_agent import extract_user_intent
from agents.discovery_agent import discover_options
from agents.eligibility_agent import is_eligible
from agents.evaluation_agent import evaluate_product
from agents.decision_agent import explain_no_match


def build_graph():
    graph = StateGraph(ShopperState)

    graph.add_node(
        "intent",
        lambda s: {"intent": extract_user_intent(s["user_query"])}
    )

    graph.add_node(
        "discover",
        lambda s: {"products": discover_options(s["intent"])}
    )

    graph.add_node(
        "filter",
        lambda s: {
            "products": [
                p for p in s.get("products", [])
                if is_eligible(s["intent"], p)
            ]
        }
    )

    graph.add_node(
        "evaluate",
        lambda s: {
            "evaluations": [
                evaluate_product(s["intent"], p)
                for p in s.get("products", [])
            ]
        }
    )

    graph.add_node(
        "decide",
        lambda s: {
            "decision": (
                explain_no_match(s["intent"])
                if not s.get("evaluations")
                else None
            )
        }
    )

    graph.set_entry_point("intent")
    graph.add_edge("intent", "discover")
    graph.add_edge("discover", "filter")
    graph.add_edge("filter", "evaluate")
    graph.add_edge("evaluate", "decide")

    return graph.compile()
