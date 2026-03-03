import streamlit as st
import joblib
import urllib.parse
import difflib
from rules import rule_based_check
from whois_check import get_domain_age
from urllib.parse import urlparse

# ---------------------------
# Page Config (MUST be first)
# ---------------------------
st.set_page_config(
    page_title="Fake Link Detection System",
    page_icon="🚨",
    layout="centered"
)

# ---------------------------
# Load CSS
# ---------------------------
def load_css():
    try:
        with open("assets/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

load_css()

# ---------------------------
# Load ML Model
# ---------------------------
@st.cache_resource
def load_ml():
    model = joblib.load("model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    return model, vectorizer

model, vectorizer = load_ml()

# ---------------------------
# Typosquatting Detection
# ---------------------------
# ---------------------------
# Typosquatting Detection (Improved)
# ---------------------------
# ---------------------------
# Typosquatting Detection (FINAL FIXED VERSION)
# ---------------------------
import difflib

def is_typo(domain):
    legit_domains = [
        "google",
        "facebook",
        "amazon",
        "microsoft",
        "apple",
        "paypal"
    ]

    # Get main name
    domain_name = domain.split(".")[0].lower()

    # If it contains numbers inside well-known name pattern
    for legit in legit_domains:
        # Replace common substitutions
        normalized = (
            domain_name
            .replace("0", "o")
            .replace("1", "l")
            .replace("3", "e")
            .replace("@", "a")
            .replace("$", "s")
        )

        # Direct match after normalization
        if normalized == legit and domain_name != legit:
            return True

    return False
# ---------------------------
# Final Decision Logic
# ---------------------------
# 4️⃣ final_decision()  ← PASTE HERE
def final_decision(url, fake_probability):

    risk_factors = []

    domain = extract_domain(url)

    if is_typo(domain):
        risk_factors.append("Possible typosquatting attack")

    if fake_probability > 0.7 or len(risk_factors) >= 2:
        result = "FAKE ❌"
    elif len(risk_factors) == 1:
        result = "SUSPICIOUS ⚠️"
    else:
        result = "SAFE ✅"

    age = "Unknown"

    return result, risk_factors, age
    # Typosquatting check
# 2️⃣ Domain Extraction Function (MUST BE ABOVE)
def extract_domain(url):
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    return domain
    domain = extract_domain(url)

    if is_typo(domain):
        risk_factors.append("Possible typosquatting attack")

    # Strong Rule-Based Detection
    
    if len(reasons) >= 2:
        return "FAKE ❌", reasons, age

    # ML-Based Decision
    if fake_prob >= 0.75:
        return "FAKE ❌", reasons, age
    elif fake_prob >= 0.60:
        return "SUSPICIOUS ⚠️", reasons, age
    else:
        return "SAFE ✅", reasons, age

# ---------------------------
# UI
# ---------------------------
st.title("🚨 Fake Link Detection System")
st.write("Hybrid Detection: Rule-Based + Machine Learning")

url = st.text_input("🔗 Enter a URL to analyze")

if st.button("🔍 Analyze URL"):

    if not url.startswith(("http://", "https://")):
        st.error("Please enter a valid URL starting with http:// or https://")
    else:
        # Vectorize input
        vector = vectorizer.transform([url])

        # Get ML probability safely
        try:
            probs = model.predict_proba(vector)[0]
            classes = model.classes_

            if "FAKE" in classes:
                fake_index = list(classes).index("FAKE")
                fake_probability = float(probs[fake_index])
            else:
                fake_probability = 0.5

        except:
            fake_probability = 0.5

        # Final Decision
        result, reasons, age = final_decision(url, fake_probability)

        # -----------------------
        # Display Results
        # -----------------------
        st.subheader(f"Result: {result}")

        st.write(f"🤖 ML Fake Probability: **{fake_probability * 100:.2f}%**")

        if age != -1:
            st.write(f"📅 Domain Age: **{age} days**")

        if reasons:
            st.warning("⚠️ Risk Factors Detected:")
            for r in reasons:
                st.write(f"- {r}")
        else:
            st.success("No suspicious patterns detected")

st.markdown("---")
st.caption("© Fake Link Detection | Developed by Abhishek Reddy")