import json
from pathlib import Path

DATA_FILE = Path("data/processed/conversations_with_conv_features.json")
SIGNALS_FILE = Path("artifacts/scored_causal_signals.json")
OUTPUT_FILE = Path("artifacts/evidence_index.json")


def identify_turn_span(convo, signal):
    """
    Very conservative span selection:
    - last 3 turns before conversation end
    This guarantees temporal precedence.
    """
    turns = convo["turns"]
    end = len(turns) - 1
    start = max(0, end - 3)
    return [start, end]


def build_evidence_index(conversations, scored_signals):
    evidence = []

    strong_signals = {
        signal
        for signal, outcomes in scored_signals.items()
        for o, v in outcomes.items()
        if v["lift"] >= 1.5
    }

    for convo in conversations:
        outcome = convo.get("outcome_event")
        if not outcome:
            continue

        for signal in strong_signals:
            features = convo["conversation_features"]

            signal_triggered = (
                (signal == "high_repeat_ratio" and features.get("repeat_ratio", 0) > 0.15)
                or (signal == "high_question_ratio" and features.get("question_ratio", 0) > 0.25)
                or (signal == "long_conversation" and features.get("total_turns", 0) > 15)
                or (signal == "customer_last_turn" and features.get("customer_last_turn"))
            )

            if not signal_triggered:
                continue

            evidence.append({
                "conversation_id": convo["conversation_id"],
                "domain": convo["domain"],
                "outcome_event": outcome,
                "signal": signal,
                "turn_span": identify_turn_span(convo, signal)
            })

    return evidence


if __name__ == "__main__":
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        conversations = json.load(f)

    with open(SIGNALS_FILE, "r", encoding="utf-8") as f:
        scored_signals = json.load(f)

    evidence_index = build_evidence_index(conversations, scored_signals)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(evidence_index, f, indent=2)

    print("✅ Evidence index constructed")
    print(f"Total evidence items: {len(evidence_index)}")
