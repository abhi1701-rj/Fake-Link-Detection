import joblib
import urllib.parse
from rules import rule_based_check
from whois_check import get_domain_age

# Load ML model and vectorizer
def load_ml():
    model = joblib.load("model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    return model, vectorizer

model, vectorizer = load_ml()

# Final decision logic
def final_decision(url, ml_conf):
    reasons = rule_based_check(url)

    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc.replace("www.", "")

    try:
        age = get_domain_age(domain)
    except:
        age = -1

    if age != -1 and age < 180:
        reasons.append("Newly registered domain")

    if len(reasons) >= 2:
        return "FAKE ❌", reasons, age

    if ml_conf < 0.7:
        return "SUSPICIOUS ⚠️", reasons, age

    return "SAFE ✅", reasons, age

# -------- MAIN PROGRAM --------
if __name__ == "__main__":

    print("🚨 Fake Link Detection System (CLI Version)")
    print("-" * 45)

    url = input("Enter a URL to analyze: ").strip()

    if not url.startswith(("http://", "https://")):
        print("❌ Invalid URL. Please include http or https")
    else:
        # ML Prediction
        vector = vectorizer.transform([url])
        prediction = model.predict(vector)[0]

        try:
            confidence = max(model.predict_proba(vector)[0])
        except:
            confidence = 0.5

        # Final decision
        result, reasons, age = final_decision(url, confidence)

        # Output
        print("\nResult:", result)
        print(f"ML Confidence: {confidence:.2f}")

        if age != -1:
            print(f"Domain Age: {age} days")

        if reasons:
            print("\n⚠️ Risk Factors Detected:")
            for r in reasons:
                print("-", r)
        else:
            print("\n✅ No suspicious patterns detected")
