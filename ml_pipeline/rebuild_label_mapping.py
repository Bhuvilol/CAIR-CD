import json
from sklearn.preprocessing import LabelEncoder

TRAIN_PATH = "EDA/clean_train_dataset.json"
OUT_PATH = "artifacts/label_mapping.json"

# Load training data
with open(TRAIN_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract labels (intents)
labels = [obj["intent"] for obj in data["transcripts"]]

# Rebuild encoder deterministically
le = LabelEncoder()
le.fit(labels)

# Save mapping: index -> label
label_mapping = {int(i): label for i, label in enumerate(le.classes_)}

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(label_mapping, f, indent=2)

print("✅ label_mapping.json rebuilt successfully")
print(label_mapping)
