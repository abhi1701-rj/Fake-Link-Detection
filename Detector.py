import streamlit as st
import joblib
import urllib.parse
import difflib
from rules import rule_based_check
from whois_check import get_domain_age

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
# Page Config (MUST be first Streamlit command)
# ---------------------------
st.set_page_config(
    page_title="Fake Link Detection System",
    page_icon="🚨",
    layout="centered"
)

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
def is_typo(domain):
    legit_domains = [
        "google.com",
        "facebook.com",
        "amazon.com",
        "microsoft.com",
        "apple.com"
    ]

    for legit in legit_domains:
        similarity = difflib.SequenceMatcher(None, domain, legit).ratio()
        if similarity > 0.8 and domain != legit:
            return True

    return False

# ---------------------------
# Final Decision Logic
# ---------------------------
def final_decision(url, fake_prob):
    reasons = rule_based_check(url)

    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc.replace("www.", "")

    # Domain age check
    age = get_domain_age(domain)
    if age != -1 and age < 180:
        reasons.append("Newly registered domain (less than 6 months old)")

    # Typosquatting check
    if is_typo(domain):
        reasons.append("Possible typosquatting attack")

    # -----------------------
    # Strong Rule-Based Detection
    # -----------------------
    if len(reasons) >= 2:
        return "FAKE ❌", reasons, age

    # -----------------------
    # ML-Based Decision
    # -----------------------
    if fake_prob >= 0.70:
        return "FAKE ❌", reasons, age
    elif fake_prob >= 0.40:
        return "SUSPICIOUS ⚠️", reasons, age
    else:
        return "SAFE ✅", reasons, age

# ---------------------------
# UI
# ---------------------------
st.title("🚨 Fake Link Detection System")
st.write("Hybrid Detection: Rule-based + Machine Learning")

url = st.text_input("🔗 Enter a URL to analyze", "https://www.google.com")

if st.button("🔍 Analyze URL"):

    if not url.startswith(("http://", "https://")):
        st.error("Please enter a valid URL starting with http:// or https://")
    else:
        # Vectorize
        vector = vectorizer.transform([url])

        # Get probabilities
        try:
            probs = model.predict_proba(vector)[0]
            classes = model.classes_

            if "FAKE" in classes:
                fake_index = list(classes).index("FAKE")
                fake_probability = probs[fake_index]
            else:
                fake_probability = 0.5

        except:
            fake_probability = 0.5

        # Final Result
        result, reasons, age = final_decision(url, fake_probability)

        # -----------------------
        # Display Results
        # -----------------------
        st.subheader(f"Result: {result}")

        st.write(f"🔐 Fake Probability: **{fake_probability:.2f}**")

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