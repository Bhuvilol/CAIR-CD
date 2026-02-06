import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from counterfactual.counterfactual_rules import COUNTERFACTUAL_RULES

def generate_counterfactuals(context, top_k=2):
    if not context.has_context():
        return {"error": "No prior context available for counterfactual analysis."}

    last = context.last_result
    factors = last.get("causal_factors", [])[:top_k]

    counterfactuals = []
    for f in factors:
        rule = COUNTERFACTUAL_RULES.get(f)
        if rule:
            counterfactuals.append({
                "target_factor": f,
                "intervention": rule["intervention"],
                "expected_change": rule["expected_change"],
                "estimated_effect": rule["estimated_effect"]
            })

    return {
        "question": "What would have prevented this outcome?",
        "counterfactuals": counterfactuals
    }
