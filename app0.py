import streamlit as st
import pandas as pd
import joblib
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Fake Link Detection System",
    page_icon="🚨",
    layout="centered"
)

st.title("🚨 Fake Link Detection System")
st.subheader("Detect malicious URLs instantly using Machine Learning")

# -------------------------------
# TRAIN MODEL IF NOT EXISTS
# -------------------------------
MODEL_FILE = "model.pkl"
VECT_FILE = "vectorizer.pkl"
DATASET_FILE = "url_dataset.csv"

def train_model():
    data = pd.read_csv(DATASET_FILE)

    X = data["url"]
    y = data["label"].map({"good": 0, "fake": 1})

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 3),
        max_features=30000,
        analyzer="char"
    )

    X_vec = vectorizer.fit_transform(X)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_vec, y)

    joblib.dump(model, MODEL_FILE)
    joblib.dump(vectorizer, VECT_FILE)

    return model, vectorizer

# -------------------------------
# LOAD OR TRAIN
# -------------------------------
if not os.path.exists(MODEL_FILE) or not os.path.exists(VECT_FILE):
    with st.spinner("Training ML model on thousands of URLs..."):
        model, vectorizer = train_model()
else:
    model = joblib.load(MODEL_FILE)
    vectorizer = joblib.load(VECT_FILE)

# -------------------------------
# UI INPUT
# -------------------------------
st.markdown("### 🔗 Enter a URL to test")

url_input = st.text_input(
    "",
    placeholder="https://example-login-secure.com"
)

# -------------------------------
# PREDICTION
# -------------------------------
if st.button("🔍 Check URL"):
    if url_input.strip() == "":
        st.warning("Please enter a URL")
    else:
        url_vec = vectorizer.transform([url_input])
        prediction = model.predict(url_vec)[0]
        probability = model.predict_proba(url_vec)[0][1]

        st.markdown("### 📌 Prediction Result")

        if prediction == 1:
            st.error("❌ This URL is FAKE / MALICIOUS")
        else:
            st.success("✅ This URL looks SAFE")

        st.markdown("### 📊 Confidence")
        st.progress(int(probability * 100))

        st.caption(f"Malicious probability: {probability:.2f}")
