# 👇 FIX: add project root to Python path
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

import streamlit as st
from graph.workflow import build_graph

st.set_page_config(page_title="Personal AI Shopper", layout="wide")

st.title("🛒 Personal AI Shopper (Phase 1)")
st.caption("Universal, reasoning-first agentic shopper powered by Gemini")

# Input
user_query = st.text_area(
    "What do you want to buy?",
    placeholder="e.g. I want something powerful but portable for ML work under 80k",
    height=120,
)

run_button = st.button("Run Shopper")

if run_button and user_query.strip():
    with st.spinner("Thinking like a smart buyer..."):
        app = build_graph()
        result = app.invoke({"user_query": user_query})

    # -------------------------
    # USER INTENT
    # -------------------------
    st.subheader("🧠 User Intent")

    intent = result["intent"]
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Product Category**")
        st.write(intent.product_category or "Not specified")

    with col2:
        st.markdown("**Budget Limit**")
        st.write(intent.budget_limit or "Not specified")

    st.markdown("**Decision Criteria**")
    for c in intent.criteria:
        st.markdown(
            f"- **{c.name}** (importance: `{c.importance}`)  \n"
            f"  _{c.description}_"
        )

    # -------------------------
    # EVALUATIONS
    # -------------------------
    st.subheader("📊 Product Evaluations")

    for ev in result["evaluations"]:
        with st.expander(f"🔹 {ev.product_name} — Score: {ev.overall_score:.2f}"):
            st.markdown("**Evaluation Factors**")
            for f in ev.factors:
                status = "✅" if f.satisfied else "❌"
                st.markdown(
                    f"{status} **{f.criterion_name}**  \n"
                    f"- Score: `{f.score}`  \n"
                    f"- Reasoning: {f.reasoning}"
                )

            if ev.risks:
                st.markdown("⚠️ **Risks / Concerns**")
                for r in ev.risks:
                    st.markdown(f"- {r}")

            st.markdown(f"🔗 [Product Link]({ev.url})")

else:
    st.info("Enter a buying request and click **Run Shopper**.")
