import streamlit as st
import json
from pathlib import Path

# -------------------------------
# Load data
# -------------------------------
CONVERSATIONS_FILE = Path("data/processed/conversations_with_conv_features.json")
EVIDENCE_FILE = Path("artifacts/evidence_index.json")

with open(CONVERSATIONS_FILE, "r", encoding="utf-8") as f:
    conversations = json.load(f)

with open(EVIDENCE_FILE, "r", encoding="utf-8") as f:
    evidence_index = json.load(f)

# -------------------------------
# Page UI
# -------------------------------
st.header("🗂️ Conversation Explorer")

st.markdown(
    """
    Explore full customer–agent conversations and inspect
    which dialogue turns were identified as **causal evidence**
    for specific outcome events.
    """
)

# -------------------------------
# Conversation selector
# -------------------------------
conversation_ids = [c["conversation_id"] for c in conversations]

selected_id = st.selectbox(
    "Select a conversation ID",
    conversation_ids
)

# Fetch selected conversation
conversation = next(
    c for c in conversations if c["conversation_id"] == selected_id
)

st.markdown("---")

# Metadata
col1, col2, col3 = st.columns(3)
col1.metric("Domain", conversation["domain"])
col2.metric("Outcome Event", conversation["outcome_event"])
col3.metric("Intent", conversation["intent"])

st.markdown("---")

# -------------------------------
# Evidence spans for this conversation
# -------------------------------
evidence_spans = [
    e["turn_span"]
    for e in evidence_index
    if e["conversation_id"] == selected_id
]

# Flatten spans to individual turn indices
highlight_turns = set()
for start, end in evidence_spans:
    for i in range(start, end + 1):
        highlight_turns.add(i)

# -------------------------------
# Transcript display
# -------------------------------
st.subheader("Conversation Transcript")

for idx, turn in enumerate(conversation["turns"]):
    speaker = turn["speaker"]
    text = turn["text"]

    if idx in highlight_turns:
        st.markdown(
            f"""
            <div style="background-color:#fff3cd;
                        padding:10px;
                        border-left:5px solid #ff9800;
                        margin-bottom:5px;">
                <strong>{speaker}</strong>: {text}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"**{speaker}**: {text}"
        )
