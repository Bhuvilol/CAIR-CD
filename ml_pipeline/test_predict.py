import json
import numpy as np
from tensorflow import keras

# Load model
MODEL_PATH = "artifacts/outcome_predictor.keras"
model = keras.models.load_model(MODEL_PATH)

# Load label mapping
with open("artifacts/label_mapping.json", "r", encoding="utf-8") as f:
    label_map = json.load(f)

# ---- TEMPORARY TEST FEATURE VECTOR ----
# Shape must match training input (770)
# 2 deterministic features + 768 embedding dims
X_dummy = np.zeros((1, model.input_shape[1]))

# Make prediction
probs = model.predict(X_dummy)
pred_idx = int(np.argmax(probs))
pred_label = label_map[str(pred_idx)]
confidence = float(probs[0][pred_idx])

print("✅ Prediction successful")
print("Predicted label:", pred_label)
print("Confidence:", round(confidence, 4))
