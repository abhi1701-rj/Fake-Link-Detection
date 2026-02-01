import joblib
import pandas as pd
from feature_registry import FEATURE_SETS

def rule_based_apk(url):
    return "❌ FAKE / PHISHING (APK detected)"

print("🔍 Smart URL Detection System (type exit to quit)")

while True:
    url = input("\nEnter URL: ").strip()
    if url.lower() == "exit":
        break

    detected = False

    for name, cfg in FEATURE_SETS.items():
        features = cfg["extract"](url)

        # Check if all required features exist
        if len(features) == len(cfg["features"]):
            detected = True

            # ML model available
            if cfg["model"]:
                model = joblib.load(cfg["model"])
                X = pd.DataFrame([features], columns=cfg["features"])
                pred = model.predict(X)[0]
                print("✅ LEGITIMATE" if pred == 1 else "❌ FAKE / PHISHING")
            else:
                print(rule_based_apk(url))

            break

    if not detected:
        print("⚠️ Unknown feature pattern — treated as suspicious")
