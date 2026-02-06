import json
from pathlib import Path

EVIDENCE_FILE = Path("artifacts/evidence_index.json")
SIGNALS_FILE = Path("artifacts/scored_causal_signals.json")


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

    relevant_evidence = [
        e for e in evidence_index if e["outcome_event"] == outcome
    ][:max_evidence]

    causal_factors = list({
        e["signal"] for e in relevant_evidence
    })

    explanation = (
        f"The outcome '{outcome}' is frequently preceded by identifiable "
        f"conversational patterns such as {', '.join(causal_factors)}. "
        f"These patterns recur across multiple conversations and appear "
        f"before the outcome event occurs."
    )

    return {
        "outcome_event": outcome,
        "causal_factors": causal_factors,
        "evidence": relevant_evidence,
        "explanation": explanation
    }


if __name__ == "__main__":
    query = "Why do escalation events occur in customer conversations?"
    result = explain_outcome(query)
    print(json.dumps(result, indent=2))
