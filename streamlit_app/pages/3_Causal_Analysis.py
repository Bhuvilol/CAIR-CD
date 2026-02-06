import streamlit as st
import json
import sys
from pathlib import Path

# --------------------------------------------------
# Path setup (so Streamlit can import your engine)
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
    Enter an analytical question about conversational outcomes.
    The system will return:
    - Evidence-grounded causal explanation
    - ML-based outcome prediction
    """
)

# --------------------------------------------------
# Query input
# --------------------------------------------------
query = st.text_input(
    "Ask a question (example: Why do escalation events occur?)",
    value="Why do escalation events occur?"
)

run = st.button("Run Analysis")

if run:
    with st.spinner("Analyzing conversations..."):
        result = answer_query(query)

    st.markdown("---")

    # --------------------------------------------------
    # Outcome
    # --------------------------------------------------
    st.subheader("Outcome Event")
    st.write(result.get("outcome_event", "N/A"))

    # --------------------------------------------------
    # Causal Factors
    # --------------------------------------------------
    st.subheader("Identified Causal Factors")
    factors = result.get("causal_factors", [])
    if factors:
        for f in factors:
            st.markdown(f"- **{f}**")
    else:
        st.info("No causal factors identified.")

    # --------------------------------------------------
    # Explanation
    # --------------------------------------------------
    st.subheader("Explanation")
    st.write(result.get("explanation", "No explanation available."))

    # --------------------------------------------------
    # ML Prediction
    # --------------------------------------------------
    ml = result.get("ml_prediction")
    if ml:
        st.subheader("ML Outcome Prediction")

        st.markdown(f"**Predicted Label:** {ml['predicted_label']}")

        confidence = ml.get("confidence", 0.0)
        st.progress(min(confidence, 1.0))
        st.caption(f"Confidence: {confidence:.3f}")

        st.info(
            "ML prediction is shown for comparison and does not replace "
            "the causal explanation."
        )

    # --------------------------------------------------
    # Evidence Summary
    # --------------------------------------------------
    st.subheader("Supporting Evidence")

    evidence = result.get("evidence", [])
    if evidence:
        for e in evidence:
            with st.expander(
                f"Conversation {e['conversation_id']} | Signal: {e['signal']}"
            ):
                st.write(f"Domain: {e['domain']}")
                st.write(f"Turn span: {e['turn_span']}")
    else:
        st.info("No evidence retrieved.")

    # --------------------------------------------------
    # Raw JSON (Transparency)
    # --------------------------------------------------
    with st.expander("Show raw system output (JSON)"):
        st.json(result)
