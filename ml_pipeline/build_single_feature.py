import json
import numpy as np
from sentence_transformers import SentenceTransformer

def build_conversation_text(convo):
    return " ".join(
        f"{turn['speaker']}: {turn['text']}"
        for turn in convo
    )

def build_feature_vector(conversation):
    # deterministic features
    total_turns = len(conversation)
    customer_turns = sum(
        1 for t in conversation if t["speaker"] == "Customer"
    )

    det_feats = np.array([
        total_turns,
        customer_turns / total_turns if total_turns else 0.0
    ])

    # semantic embedding (same model as training)
    model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
    convo_text = build_conversation_text(conversation)
    embedding = model.encode(convo_text)

    # final feature vector
    return np.concatenate([det_feats, embedding]).reshape(1, -1)
