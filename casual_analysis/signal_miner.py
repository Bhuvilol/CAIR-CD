import json
from pathlib import Path
from collections import defaultdict

INPUT_FILE = Path("data/processed/conversations_with_conv_features.json")
OUTPUT_DIR = Path("artifacts")
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "candidate_signals.json"


def mine_candidate_signals(conversations):
    signal_stats = defaultdict(lambda: defaultdict(int))

    for convo in conversations:
        outcome = convo.get("outcome_event")
        features = convo.get("conversation_features", {})

        if not outcome:
            continue

        # Simple, interpretable signals
        if features.get("repeat_ratio", 0) > 0.15:
            signal_stats["high_repeat_ratio"][outcome] += 1

        if features.get("question_ratio", 0) > 0.25:
            signal_stats["high_question_ratio"][outcome] += 1

        if features.get("total_turns", 0) > 15:
            signal_stats["long_conversation"][outcome] += 1

        if features.get("customer_last_turn"):
            signal_stats["customer_last_turn"][outcome] += 1

    return signal_stats


if __name__ == "__main__":
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        conversations = json.load(f)

    signals = mine_candidate_signals(conversations)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(signals, f, indent=2)

    print("✅ Candidate causal signals mined")
    print(f"Saved to {OUTPUT_FILE}")
