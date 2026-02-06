import json
import numpy as np
from tensorflow import keras
from .build_single_feature import build_feature_vector

MODEL_PATH = "artifacts/outcome_predictor.keras"
LABEL_PATH = "artifacts/label_mapping.json"

# load once
_model = keras.models.load_model(MODEL_PATH)

with open(LABEL_PATH, "r", encoding="utf-8") as f:
    _label_map = json.load(f)

def predict_outcome(conversation):
    """
    conversation: list of {speaker, text}
    returns: {label, confidence}
    """
    X = build_feature_vector(conversation)
    probs = _model.predict(X)[0]

    idx = int(np.argmax(probs))
    return {
        "predicted_label": _label_map[str(idx)],
        "confidence": float(probs[idx])
    }
