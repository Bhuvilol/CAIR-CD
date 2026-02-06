import json
from pathlib import Path

INPUT_FILE = Path("data/processed/conversations_with_features.json")
OUTPUT_FILE = Path("data/processed/conversations_with_conv_features.json")


def add_conversation_features(conversations):
    for convo in conversations:
        turns = convo["turns"]

        total_turns = len(turns)
        customer_turns = sum(1 for t in turns if t["speaker"] == "Customer")
        agent_turns = sum(1 for t in turns if t["speaker"] == "Agent")
        question_turns = sum(1 for t in turns if t["features"].get("is_question"))
        repeat_turns = sum(1 for t in turns if t["features"].get("is_repeat"))

        convo["conversation_features"] = {
            "total_turns": total_turns,
            "customer_turns": customer_turns,
            "agent_turns": agent_turns,
            "question_ratio": question_turns / total_turns if total_turns else 0.0,
            "repeat_ratio": repeat_turns / total_turns if total_turns else 0.0,
            "customer_last_turn": turns[-1]["speaker"] == "Customer"
        }

    return conversations


if __name__ == "__main__":
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        conversations = json.load(f)

    conversations = add_conversation_features(conversations)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(conversations, f, indent=2)

    print("✅ Conversation-level feature extraction complete")
    print(f"Saved to {OUTPUT_FILE}")
