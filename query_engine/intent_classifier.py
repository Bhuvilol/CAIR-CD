from sentence_transformers import SentenceTransformer
import numpy as np
import json
from pathlib import Path

MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
model = SentenceTransformer(MODEL_NAME)

# --------------------------------------------------
# Intent prototypes (semantic anchors)
# --------------------------------------------------
INTENT_PROTOTYPES = {
    "FACTOR_IMPORTANCE": [
        "Which factor matters most?",
        "What is the most important causal factor?",
        "Which signal dominates?"
    ],
    "TEMPORAL_PATTERN": [
        "How early does escalation occur?",
        "What happens before the outcome?",
        "Which signals appear first?"
    ],
    "DOMAIN_COMPARISON": [
        "Does this vary by domain?",
        "Is this different across industries?",
        "Which domain shows this most?"
    ],
    "COUNTERFACTUAL": [
        "What would have prevented this?",
        "How could this have been avoided?"
    ],
    "SUMMARY": [
        "Summarize the findings",
        "Give a brief explanation"
    ]
}

# --------------------------------------------------
# Precompute prototype embeddings
# --------------------------------------------------
PROTOTYPE_EMBEDDINGS = {
    intent: model.encode(texts)
    for intent, texts in INTENT_PROTOTYPES.items()
}

# --------------------------------------------------
# Intent prediction
# --------------------------------------------------
def predict_intent(query: str, threshold=0.45):
    q_emb = model.encode([query])[0]

    best_intent = None
    best_score = 0.0

    for intent, emb_list in PROTOTYPE_EMBEDDINGS.items():
        scores = np.dot(emb_list, q_emb) / (
            np.linalg.norm(emb_list, axis=1) * np.linalg.norm(q_emb)
        )
        score = float(scores.max())

        if score > best_score:
            best_score = score
            best_intent = intent

    if best_score < threshold:
        return None

    return best_intent
