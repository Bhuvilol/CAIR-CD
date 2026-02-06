import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ml_pipeline.predict_outcome import predict_outcome

EVIDENCE_FILE = Path("artifacts/evidence_index.json")
SIGNALS_FILE = Path("artifacts/scored_causal_signals.json")
CONVERSATIONS_FILE = Path("data/processed/conversations_with_conv_features.json")


def parse_outcome_from_query(query: str):
    q = query.lower()
    if "escalation" in q:
        return "Escalation"
    if "refund" in q or "replacement" in q:
        return "Compensation"
    if "fraud" in q:
        return "FraudResolution"
    return None


def explain_outcome(query: str, max_evidence=5):
    outcome = parse_outcome_from_query(query)
    if not outcome:
        return {"error": "Unable to determine outcome from query"}

    with open(EVIDENCE_FILE, "r", encoding="utf-8") as f:
        evidence_index = json.load(f)

    with open(SIGNALS_FILE, "r", encoding="utf-8") as f:
        scored_signals = json.load(f)

    with open(CONVERSATIONS_FILE, "r", encoding="utf-8") as f:
        conversations = json.load(f)

    # pick relevant evidence
    relevant_evidence = [
        e for e in evidence_index if e["outcome_event"] == outcome
    ][:max_evidence]

    causal_factors = list({e["signal"] for e in relevant_evidence})

    explanation = (
        f"The outcome '{outcome}' is frequently preceded by identifiable "
        f"conversational patterns such as {', '.join(causal_factors)}. "
        f"These patterns recur across multiple conversations and appear "
        f"before the outcome event occurs."
    )

    # ---- ML PREDICTION (minimal, grounded) ----
    ml_prediction = None
    if relevant_evidence:
        conv_id = relevant_evidence[0]["conversation_id"]
        convo = next(
            c for c in conversations if c["conversation_id"] == conv_id
        )
        ml_prediction = predict_outcome(convo["turns"])

    return {
        "outcome_event": outcome,
        "causal_factors": causal_factors,
        "evidence": relevant_evidence,
        "explanation": explanation,
        "ml_prediction": ml_prediction
    }


if __name__ == "__main__":
    query = "Why do escalation events occur in customer conversations?"
    result = explain_outcome(query)
    print(json.dumps(result, indent=2))
