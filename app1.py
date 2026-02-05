import streamlit as st
import re
import numpy as np
import pickle

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Fake Link Detection",
    page_icon="🔐",
    layout="wide"
)

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

# ---------------- FEATURE EXTRACTION ----------------
def extract_features(url):
    return np.array([[
        len(url),
        url.count('.'),
        url.count('/'),
        1 if url.startswith("https") else 0,
        1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 0,
        sum(char.isdigit() for char in url),
        len(re.findall(r"[@?=&]", url)),
        url.count('-'),
        url.count('sub')
    ]])

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #020617);
}

.hero {
    background: linear-gradient(135deg, #2563eb, #1e3a8a);
    padding: 60px;
    border-radius: 24px;
    color: white;
    margin-bottom: 40px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}

.card {
    background: #020617;
    padding: 30px;
    border-radius: 20px;
    color: white;
    box-shadow: 0 15px 30px rgba(0,0,0,0.4);
}

.stTextInput input {
    border-radius: 12px;
    padding: 12px;
}

.stButton button {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    color: white;
    border-radius: 12px;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: bold;
    border: none;
}

.footer {
    text-align: center;
    color: #94a3b8;
    margin-top: 60px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
    <h1>🚨 Fake Link Detection System</h1>
    <p style="font-size:18px;">
        Detect phishing and malicious URLs instantly using Machine Learning.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- MAIN CONTENT ----------------
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔎 Analyze a URL")

    url = st.text_input("Enter URL", placeholder="https://example.com")

    if st.button("Analyze URL"):
        if not url.strip():
            st.warning("Please enter a valid URL")
        else:
            features = extract_features(url)
            prediction = model.predict(features)[0]

            if prediction == 1:
                st.success("✅ This URL looks SAFE")
            else:
                st.error("❌ This URL looks FAKE")

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Features Used")
    st.write("""
    • URL length  
    • Dot count  
    • Slash count  
    • HTTPS usage  
    • IP address detection  
    • Digit count  
    • Special characters  
    • Hyphen usage  
    • Subdomain patterns  
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
© 2026 Fake Link Detection | Developed by Abhishek Reddy
</div>
""", unsafe_allow_html=True)
