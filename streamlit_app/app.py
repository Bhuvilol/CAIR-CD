import streamlit as st

st.set_page_config(
    page_title="CAIR Studio",
    layout="wide"
)

st.title("CAIR Studio")
st.subheader("Causal Analysis & Interactive Reasoning over Conversations")

st.markdown(
    """
    **CAIR Studio** is an interactive observability dashboard for:
    - Conversational causal analysis
    - Evidence-grounded explanations
    - ML-based outcome prediction
    - Multi-turn analytical reasoning
    - Counterfactual prevention insights

    Use the sidebar to explore each component of the system.
    """
)

st.info(
    "This dashboard visualizes a complete end-to-end system — "
    "from raw conversations to causal explanations and counterfactual reasoning."
)
