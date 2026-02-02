import streamlit as st
import joblib
import os
import numpy as np
from feature_extraction import extract_features

# Load model
MODEL_PATH = "rf_basic.pkl"
model = joblib.load(MODEL_PATH)

st.set_page_config(page_title="Fake Link Detection", page_icon="🔐")

st.title("🔐 Fake Link Detection System")
st.write("Enter a URL to check whether it is **Safe** or **Phishing**.")

url = st.text_input("Enter URL")

if st.button("Check URL"):
    if url.strip() == "":
        st.warning("Please enter a URL")
    else:
        features = extract_features(url)
        features = np.array(features).reshape(1, -1)

        prediction = model.predict(features)[0]

        if prediction == 1:
            st.error("⚠️ Phishing / Fake Link Detected")
        else:
            st.success("✅ This link looks Safe")
