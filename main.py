from graph.workflow import build_graph

if __name__ == "__main__":
    app = build_graph()

    result = app.invoke({
        "user_query": "I want something powerful but portable for ML work under 80k"
    })

    print("\n=== USER INTENT ===")
    print(result["intent"])

    print("\n=== EVALUATIONS ===")
    if result.get("evaluations"):
        for ev in result["evaluations"]:
            print(ev)

    if result.get("decision"):
        print("\n=== DECISION ===")
        print(result["decision"])
