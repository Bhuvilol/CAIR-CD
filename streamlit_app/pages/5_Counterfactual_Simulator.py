import streamlit as st
import sys
from pathlib import Path

# --------------------------------------------------
# Path setup
# --------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from query_engine.task1_explainer import answer_query

# --------------------------------------------------
# Page UI
# --------------------------------------------------
st.header("🔁 Counterfactual Simulator")

st.markdown(
    """
    Explore **what changes could have prevented a negative outcome**.

    This simulator is **self-contained** and guarantees results
    even if other pages were not visited.
    """
)

st.markdown("---")

# --------------------------------------------------
# Ensure causal analysis ALWAYS exists
# --------------------------------------------------
if "last_analysis" not in st.session_state:
    with st.spinner("Preparing causal analysis..."):
        analysis = answer_query("Why do escalation events occur?")
        st.session_state["last_analysis"] = analysis
else:
    analysis = st.session_state["last_analysis"]

# --------------------------------------------------
# Display analysis summary
# --------------------------------------------------
st.subheader("Analyzed Outcome")
st.markdown(f"**Outcome:** {analysis.get('outcome_event', 'Escalation')}")

factors = analysis.get("causal_factors", [])
if factors:
    st.markdown("**Causal Factors:** " + ", ".join(factors))

st.markdown("---")

# --------------------------------------------------
# Generate counterfactuals
# --------------------------------------------------
if st.button("Generate Counterfactuals"):
    with st.spinner("Simulating preventive interventions..."):
        counterfactuals = answer_query(
            "What would have prevented this outcome?"
        )

    st.session_state["last_counterfactual"] = counterfactuals

# --------------------------------------------------
# Display counterfactuals
# --------------------------------------------------
if "last_counterfactual" in st.session_state:
    response = st.session_state["last_counterfactual"]

    st.subheader("Counterfactual Interventions")

    for idx, cf in enumerate(response.get("counterfactuals", []), 1):
        with st.expander(f"Intervention {idx}: {cf['target_factor']}"):
            st.markdown(
                f"""
                **Target Factor:** `{cf['target_factor']}`  
                **Suggested Action:** {cf['intervention']}  
                **Expected Effect:** {cf['estimated_effect']}
                """
            )

    with st.expander("Raw counterfactual output"):
        st.json(response)
