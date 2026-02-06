import json
from pathlib import Path

# -------- CONFIG --------
RAW_DATA_PATH = Path("data/raw/Conversational_Transcript_Dataset.json")

REQUIRED_CONVO_FIELDS = {
    "transcript_id",
    "domain",
    "intent",
    "conversation"
}

VALID_SPEAKERS = {"Agent", "Customer"}


def load_raw_dataset(path=RAW_DATA_PATH):
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "transcripts" not in data:
        raise ValueError("Top-level key 'transcripts' not found")

    return data["transcripts"]


def validate_dataset(conversations):
    total_turns = 0

    for idx, convo in enumerate(conversations):
        missing = REQUIRED_CONVO_FIELDS - convo.keys()
        if missing:
            raise ValueError(
                f"Conversation {idx} missing required fields: {missing}"
            )

        turns = convo["conversation"]
        if not isinstance(turns, list) or len(turns) == 0:
            raise ValueError(f"Conversation {idx} has no turns")

        for t_idx, turn in enumerate(turns):
            speaker = turn.get("speaker")
            text = turn.get("text")

            if speaker not in VALID_SPEAKERS:
                raise ValueError(
                    f"Invalid speaker '{speaker}' at convo {idx}, turn {t_idx}"
                )

            if not isinstance(text, str) or not text.strip():
                raise ValueError(
                    f"Invalid text at convo {idx}, turn {t_idx}"
                )

        total_turns += len(turns)

    return {
        "num_conversations": len(conversations),
        "num_turns": total_turns
    }


if __name__ == "__main__":
    conversations = load_raw_dataset()
    stats = validate_dataset(conversations)

    print("✅ Dataset validation successful")
    print(f"Conversations: {stats['num_conversations']}")
    print(f"Total turns: {stats['num_turns']}")
