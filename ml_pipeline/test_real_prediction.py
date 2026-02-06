import json
import numpy as np
from tensorflow import keras
from build_single_feature import build_feature_vector

# Load model
model = keras.models.load_model("artifacts/outcome_predictor.keras")

# Load label mapping
with open("artifacts/label_mapping.json", "r") as f:
    label_map = json.load(f)

# Load ONE real conversation (test split)
with open("EDA/clean_test_dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

sample = data["transcripts"][0]

# Build feature vector
X = build_feature_vector(sample["conversation"])

# Predict
probs = model.predict(X)
pred_idx = int(np.argmax(probs))
pred_label = label_map[str(pred_idx)]
confidence = float(probs[0][pred_idx])

print("✅ Real prediction successful")
print("Predicted label:", pred_label)
print("Confidence:", round(confidence, 4))
