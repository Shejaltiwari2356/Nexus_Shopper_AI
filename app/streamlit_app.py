import streamlit as st
import pandas as pd
import os, sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)
from graph.workflow import build_graph

st.set_page_config(page_title="Nexus Shopper AI", layout="wide")
st.title("🛒 Nexus Shopper AI")

user_query = st.text_area("What are you looking for?", placeholder="e.g. 10 best noise cancelling headphones under 15k", height=100)

if st.button("Start Analysis") and user_query.strip():
    with st.spinner("Finding 10 options and comparing offers..."):
        app = build_graph()
        result = app.invoke({"user_query": user_query})

    if result.get("recommendation"):
        rec = result["recommendation"]
        st.success(f"### 🏆 Top Pick: {rec.best_choice}")
        st.write(rec.justification)

    st.divider()
    st.subheader("📊 Comparative Market Analysis")
    if result.get("evaluations"):
        # Comparison Table
        df_data = [{
            "Product": ev.product_name,
            "Price": f"₹{ev.price}",
            "Platform": ev.platform,
            "Score": ev.overall_score,
            "Specs": ev.summary_specs
        } for ev in result["evaluations"]]
        st.table(pd.DataFrame(df_data))

        # Detailed Breakdown
        for ev in result["evaluations"]:
            with st.expander(f"🔍 {ev.product_name} - Full Specifications"):
                c1, c2 = st.columns(2)
                with c1: st.markdown(f"**Technical Specs:**\n{ev.detailed_specs}")
                with c2: st.markdown(f"**Offer Analysis:**\n{ev.offer_analysis}")
                st.markdown(f"🔗 [View Product Page]({ev.url})")
    elif result.get("decision"):
        st.warning(result["decision"])