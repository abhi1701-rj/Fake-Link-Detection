from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from backend.features.basic_features import extract, FEATURE_NAMES

# Create FastAPI app
app = FastAPI(title="Fake Link Detection API")

# Load your trained model
model = joblib.load("backend/models/rf_basic.pkl")

# Define input structure
class URLItem(BaseModel):
    url: str

# API endpoint
@app.post("/predict")
def predict_url(item: URLItem):
    # Extract features
    features_dict = extract(item.url)
    X = pd.DataFrame([[features_dict[name] for name in FEATURE_NAMES]], columns=FEATURE_NAMES)

    # Predict
    pred = model.predict(X)[0]
    result = "LEGITIMATE" if pred == 1 else "FAKE / PHISHING"
    
    return {"url": item.url, "prediction": result}
