import streamlit as st
import sys
from pathlib import Path

# --------------------------------------------------
# Helper (must be defined BEFORE use)
# --------------------------------------------------
def json_to_text(resp):
    if isinstance(resp, dict):
        if "answer" in resp:
            return resp["answer"]
        if "explanation" in resp:
            return resp["explanation"]
    return str(resp)

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
st.header("💬 Multi-Turn Analytical Query")

st.markdown(
    """
    This interface demonstrates **context-aware reasoning**.
    Follow-up questions build upon prior system responses
    without recomputing from scratch.
    """
)

# --------------------------------------------------
# Session state
# --------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --------------------------------------------------
# Display chat history
# --------------------------------------------------
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --------------------------------------------------
# Input box
# --------------------------------------------------
query = st.chat_input("Ask a question…")

if query:
    # User message
    st.session_state.chat_history.append(
        {"role": "user", "content": query}
    )

    with st.chat_message("assistant"):
        with st.spinner("Reasoning…"):
            response = answer_query(query)

        # Render response nicely
        if isinstance(response, dict):
            if "answer" in response:
                st.markdown(response["answer"])
            else:
                st.markdown(response.get("explanation", ""))
                ml = response.get("ml_prediction")
                if ml:
                    st.caption(
                        f"ML Prediction: {ml['predicted_label']} "
                        f"(confidence {ml['confidence']:.2f})"
                    )
        else:
            st.markdown(str(response))

    # Store assistant response in history
    st.session_state.chat_history.append(
        {"role": "assistant", "content": json_to_text(response)}
    )
