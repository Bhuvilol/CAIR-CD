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
st.header("🧠 Causal Analysis & Outcome Prediction")

st.markdown(
    """
    Ask an analytical question about conversational outcomes.
    The system returns **causal explanations**, **evidence**, and
    **ML-based predictions**.
    """
)

query = st.text_input(
    "Ask a question",
    value="Why do escalation events occur?"
)

run = st.button("Run Analysis")

if run:
    with st.spinner("Analyzing conversations..."):
        result = answer_query(query)

    # 🔐 Persist analysis for other pages
    st.session_state["last_analysis"] = result
    st.session_state["analysis_ready"] = True

    st.markdown("---")

    st.subheader("Outcome Event")
    st.write(result.get("outcome_event", "N/A"))

    st.subheader("Causal Factors")
    for f in result.get("causal_factors", []):
        st.markdown(f"- **{f}**")

    st.subheader("Explanation")
    st.write(result.get("explanation", ""))

    ml = result.get("ml_prediction")
    if ml:
        st.subheader("ML Prediction")
        st.markdown(f"**Label:** {ml['predicted_label']}")
        st.progress(min(ml["confidence"], 1.0))
        st.caption(f"Confidence: {ml['confidence']:.3f}")

    st.subheader("Evidence")
    for e in result.get("evidence", []):
        with st.expander(
            f"{e['conversation_id']} | {e['signal']}"
        ):
            st.write(f"Domain: {e['domain']}")
            st.write(f"Turn span: {e['turn_span']}")

    with st.expander("Raw JSON output"):
        st.json(result)
