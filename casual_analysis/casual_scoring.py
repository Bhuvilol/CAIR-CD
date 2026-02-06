import json
from pathlib import Path
from collections import defaultdict

SIGNALS_FILE = Path("artifacts/candidate_signals.json")
DATA_FILE = Path("data/processed/conversations_with_conv_features.json")
OUTPUT_FILE = Path("artifacts/scored_causal_signals.json")


def load_total_outcomes(conversations):
    outcome_counts = defaultdict(int)
    total = 0

    for convo in conversations:
        outcome = convo.get("outcome_event")
        if outcome:
            outcome_counts[outcome] += 1
            total += 1

    return outcome_counts, total


def score_signals(candidate_signals, outcome_counts, total_outcomes):
    scored = {}

    for signal, outcomes in candidate_signals.items():
        scored[signal] = {}

        total_signal_occurrences = sum(outcomes.values())

        for outcome, count in outcomes.items():
            p_signal_given_outcome = count / outcome_counts[outcome]
            p_signal_overall = total_signal_occurrences / total_outcomes

            lift = round(p_signal_given_outcome / p_signal_overall, 3)

            scored[signal][outcome] = {
                "count": count,
                "lift": lift
            }

    return scored


if __name__ == "__main__":
    with open(SIGNALS_FILE, "r", encoding="utf-8") as f:
        candidate_signals = json.load(f)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        conversations = json.load(f)

    outcome_counts, total_outcomes = load_total_outcomes(conversations)

    scored_signals = score_signals(
        candidate_signals,
        outcome_counts,
        total_outcomes
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(scored_signals, f, indent=2)

    print("✅ Causal signals scored and filtered")
    print(f"Saved to {OUTPUT_FILE}")
