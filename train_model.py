# train_model.py

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

# -------------------------
# Step 1: Load your dataset
# -------------------------
# Replace 'data.csv' with your dataset path
df = pd.read_csv("data.csv")

# -------------------------
# Step 2: Select EXACT FEATURES
# -------------------------
FEATURES = [
    "url_length",
    "count_dots",
    "count_slash",
    "has_https",
    "has_ip",
    "digit_count",
    "special_char_count",
    "suspicious_words",
    "subdomain_count"
]

TARGET = "label"  # replace with your target column name, e.g., 0=Fake, 1=Safe

X = df[FEATURES]
y = df[TARGET]

# -------------------------
# Step 3: Split the dataset
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------
# Step 4: Train the model
# -------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# -------------------------
# Step 5: Logs for debugging
# -------------------------
print("=== TRAINING LOGS ===")
print("Feature names:", FEATURES)
print("Number of features:", model.n_features_in_)
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)

y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
print("=====================")

# -------------------------
# Step 6: Save model
# -------------------------
joblib.dump(model, "model.pkl")
print("Model saved as 'model.pkl'")
