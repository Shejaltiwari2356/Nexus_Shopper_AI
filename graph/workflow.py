from langgraph.graph import StateGraph, END
from graph.state import ShopperState
from agents.consultant_agent import extract_user_intent
from agents.discovery_agent import discover_options
from agents.eligibility_agent import is_eligible
from agents.evaluation_agent import evaluate_product
from agents.decision_agent import explain_no_match
from agents.recommendation_agent import recommend

def build_graph():
    graph = StateGraph(ShopperState)

    graph.add_node("intent", lambda s: {"intent": extract_user_intent(s["user_query"])})
    graph.add_node("discover", lambda s: {"products": discover_options(s["intent"])})
    graph.add_node("filter", lambda s: {"products": [p for p in s.get("products", []) if is_eligible(s["intent"], p)]})

    def evaluate_node(s):
        top_matches = s.get("products", [])[:10] # Scale to 10 options
        if not top_matches: return {"evaluations": []}
        return {"evaluations": [evaluate_product(s["intent"], p) for p in top_matches]}
    
    graph.add_node("evaluate", evaluate_node)
    graph.add_node("recommend", lambda s: {"recommendation": recommend(s["evaluations"])})
    graph.add_node("decide_fallback", lambda s: {"decision": explain_no_match(s["intent"])})

    graph.set_entry_point("intent")
    graph.add_edge("intent", "discover")
    graph.add_edge("discover", "filter")
    graph.add_edge("filter", "evaluate")

    graph.add_conditional_edges("evaluate", lambda s: "recommend" if s.get("evaluations") else "decide_fallback", {
        "recommend": "recommend",
        "decide_fallback": "decide_fallback"
    })

    graph.add_edge("recommend", END)
    graph.add_edge("decide_fallback", END)
    return graph.compile()