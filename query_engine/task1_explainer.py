import json
import sys
from pathlib import Path

# ------------------------------------------------------------------
# Path setup (repo root)
# ------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# ------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------
from context_memory.analysis_context import AnalysisContext
from query_engine.followup_handler import handle_followup
from ml_pipeline.predict_outcome import predict_outcome
from counterfactual.counterfactual_engine import generate_counterfactuals

# ------------------------------------------------------------------
# File paths
# ------------------------------------------------------------------
EVIDENCE_FILE = Path("artifacts/evidence_index.json")
SIGNALS_FILE = Path("artifacts/scored_causal_signals.json")
CONVERSATIONS_FILE = Path("data/processed/conversations_with_conv_features.json")

# ------------------------------------------------------------------
# Global deterministic context (Task 2)
# ------------------------------------------------------------------
context = AnalysisContext()

# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
def parse_outcome_from_query(query: str):
    q = query.lower()
    if "escalation" in q:
        return "Escalation"
    if "refund" in q or "replacement" in q:
        return "Compensation"
    if "fraud" in q:
        return "FraudResolution"
    return None


# ------------------------------------------------------------------
# Task 1: Query-driven causal explanation + ML prediction
# ------------------------------------------------------------------
def explain_outcome(query: str, max_evidence: int = 5):
    outcome = parse_outcome_from_query(query)
    if not outcome:
        return {"error": "Unable to determine outcome from query"}

    with open(EVIDENCE_FILE, "r", encoding="utf-8") as f:
        evidence_index = json.load(f)

    with open(SIGNALS_FILE, "r", encoding="utf-8") as f:
        scored_signals = json.load(f)

    with open(CONVERSATIONS_FILE, "r", encoding="utf-8") as f:
        conversations = json.load(f)

    # Select evidence relevant to the queried outcome
    relevant_evidence = [
        e for e in evidence_index if e["outcome_event"] == outcome
    ][:max_evidence]

    # Extract causal factors
    causal_factors = list({e["signal"] for e in relevant_evidence})

    # Natural language explanation
    explanation = (
        f"The outcome '{outcome}' is frequently preceded by identifiable "
        f"conversational patterns such as {', '.join(causal_factors)}. "
        f"These patterns recur across multiple conversations and appear "
        f"before the outcome event occurs."
    )

    # --------------------------------------------------------------
    # ML prediction (grounded in one evidenced conversation)
    # --------------------------------------------------------------
    ml_prediction = None
    if relevant_evidence:
        conv_id = relevant_evidence[0]["conversation_id"]
        convo = next(
            c for c in conversations if c["conversation_id"] == conv_id
        )
        ml_prediction = predict_outcome(convo["turns"])

    # Final result object
    result = {
        "outcome_event": outcome,
        "causal_factors": causal_factors,
        "evidence": relevant_evidence,
        "explanation": explanation,
        "ml_prediction": ml_prediction
    }

    # Update deterministic context (Task 2)
    context.update(query, result)

    return result


# ------------------------------------------------------------------
# Task 2 + Baby Step 9: Context-aware routing
# ------------------------------------------------------------------
def answer_query(query: str):
    q = query.lower()

    # Counterfactual queries (Baby Step 9)
    if context.has_context() and (
        "prevent" in q or "avoided" in q or "counterfactual" in q
    ):
        return generate_counterfactuals(context)

    # Follow-up analytical queries (Task 2)
    if context.has_context() and query.strip().endswith("?"):
        return handle_followup(query, context)

    # Fresh analytical query (Task 1)
    return explain_outcome(query)


# ------------------------------------------------------------------
# Manual test entry point
# ------------------------------------------------------------------
if __name__ == "__main__":
    q1 = "Why do escalation events occur?"
    print("Q1:", q1)
    print(json.dumps(answer_query(q1), indent=2))

    q2 = "Which factor matters most?"
    print("\nQ2:", q2)
    print(json.dumps(answer_query(q2), indent=2))

    q3 = "What would have prevented this escalation?"
    print("\nQ3:", q3)
    print(json.dumps(answer_query(q3), indent=2))
