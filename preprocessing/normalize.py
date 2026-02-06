import json
from pathlib import Path
from ingest_validate import load_raw_dataset

PROCESSED_DATA_PATH = Path("data/processed")
PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = PROCESSED_DATA_PATH / "conversations.json"


def map_outcome_event(intent: str):
    intent_lower = intent.lower()
    if "escalation" in intent_lower:
        return "Escalation"
    if "refund" in intent_lower or "replacement" in intent_lower:
        return "Compensation"
    return None


def normalize_conversations(raw_conversations):
    normalized = []

    for convo in raw_conversations:
        convo_obj = {
            "conversation_id": convo["transcript_id"],
            "domain": convo.get("domain"),
            "intent": convo.get("intent"),
            "outcome_event": map_outcome_event(convo.get("intent", "")),
            "timestamp": convo.get("time_of_interaction"),
            "turns": []
        }

        for idx, turn in enumerate(convo["conversation"]):
            turn_obj = {
                "turn_id": idx,
                "speaker": turn["speaker"],
                "text": turn["text"],
                "position": idx,
                "timestamp": None,
                "features": {}
            }
            convo_obj["turns"].append(turn_obj)

        normalized.append(convo_obj)

    return normalized


if __name__ == "__main__":
    raw_conversations = load_raw_dataset()
    normalized = normalize_conversations(raw_conversations)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(normalized, f, indent=2)

    print("✅ Normalization complete")
    print(f"Saved {len(normalized)} conversations to {OUTPUT_FILE}")
