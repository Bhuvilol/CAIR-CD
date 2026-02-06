from tensorflow import keras

MODEL_PATH = "artifacts/outcome_predictor.keras"

model = keras.models.load_model(MODEL_PATH)

print("✅ Model loaded successfully")
model.summary()
