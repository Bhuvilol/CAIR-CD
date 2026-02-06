import streamlit as st

st.header("📊 System Overview")

st.markdown(
    """
    ### What does this system do?

    This system analyzes large-scale **customer–agent conversations**
    to answer three critical questions:

    1. **Why did a costly outcome occur?**  
       (Causal explanation with evidence)

    2. **How confident are we?**  
       (ML-based outcome prediction)

    3. **What would have prevented it?**  
       (Counterfactual replay and intervention analysis)
    """
)

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Conversations", "5,037")
col2.metric("Total Turns", "84,465")
col3.metric("Outcome Events", "Escalations / Refunds")
col4.metric("Model Type", "MPNet + Keras")

st.markdown("---")

st.markdown(
    """
    ### System Architecture

    **Pipeline Overview**
    ```
    Conversations
        ↓
    Feature Extraction
        ↓
    Causal Signal Mining
        ↓
    Evidence Indexing
        ↓
    ML Outcome Prediction
        ↓
    Multi-turn Reasoning
        ↓
    Counterfactual Prevention
    ```
    """
)

st.success(
    "This dashboard is fully grounded in real data, "
    "with all explanations traceable to concrete conversation evidence."
)
