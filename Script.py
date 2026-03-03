import pandas as pd
import re
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=200)
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load dataset
data = pd.read_csv("phishing_dataset.csv")

# Feature extraction
def extract_features(url):
    return [
        len(url),
        url.count('.'),
        url.count('-'),
        sum(c.isdigit() for c in url),
        int("@" in url),
        int("https" in url),
        int(bool(re.search(r'\d+\.\d+\.\d+\.\d+', url)))
    ]

data["features"] = data["url"].apply(extract_features)

X_text = data["url"]
X_features = np.array(data["features"].tolist())
y = data["label"]

# Vectorize URL text
vectorizer = TfidfVectorizer(ngram_range=(1,2))
X_text_vec = vectorizer.fit_transform(X_text)

# Combine text + numeric features
from scipy.sparse import hstack
X_final = hstack([X_text_vec, X_features])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X_final, y, test_size=0.2, random_state=42
)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")