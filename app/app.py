from joblib import load
import streamlit as st
import joblib
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(_file_), "..")))

from backend.features.feature_extraction import extract_features
MODEL_PATH = os.path.join(os.path.dirname(__file__),"..","backend","models","rf_basic.pkl")
# Allow app to access backend folder
sys.path.append(os.path.abspath("../backend"))

from feature_extraction import extract_features

model = joblib.load("../backend/model.pkl")
model = load("models/rf_basic.pkl")

columns = [
    "url_length",
    "has_https",
    "has_ip",
    "has_at",
    "dot_count",
    "digit_count",
    "has_hyphen",
    "is_shortened"
]

st.set_page_config(page_title="Fake Link Detection", layout="centered")

st.title("🔐 Fake Link Detection System")
st.write("Enter a URL to check whether it is **Legitimate or Phishing**")

url = st.text_input("Enter URL")

if st.button("Check URL"):
    if url.strip() == "":
        st.warning("Please enter a URL")
    else:
        features = extract_features(url)
        X = pd.DataFrame([features], columns=columns)
        prediction = model.predict(X)[0]

        if prediction == 1:
            st.error("❌ FAKE / PHISHING URL")
        else:
            st.success("✅ LEGITIMATE URL")
