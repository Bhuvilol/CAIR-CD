import json
from pathlib import Path

INPUT_FILE = Path("data/processed/conversations.json")
OUTPUT_FILE = Path("data/processed/conversations_with_features.json")


def extract_turn_features(conversations):
    for convo in conversations:
        seen_texts = set()

        for turn in convo["turns"]:
            text = turn["text"]

            features = {
                "token_count": len(text.split()),
                "is_question": text.strip().endswith("?"),
                "is_repeat": text in seen_texts
            }

            seen_texts.add(text)
            turn["features"] = features

    return conversations


if __name__ == "__main__":
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        conversations = json.load(f)

    conversations = extract_turn_features(conversations)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(conversations, f, indent=2)

    print("✅ Turn-level feature extraction complete")
    print(f"Saved to {OUTPUT_FILE}")
