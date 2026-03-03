import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ===============================
# 1. Load Dataset
# ===============================

data = pd.read_csv("phishing_dataset.csv")

# Keep required columns
data = data[['url', 'label']]

print("Total URLs in dataset:", len(data))
print("Class Distribution:\n", data['label'].value_counts())

# ===============================
# 2. Split Dataset (Balanced)
# ===============================

X = data['url']
y = data['label']

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y   # ensures both classes appear in train & test
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

# ===============================
# 3. Feature Extraction
# ===============================

vectorizer = TfidfVectorizer(
    analyzer='char',
    ngram_range=(2, 4)
)

X_train_vector = vectorizer.fit_transform(X_train)
X_test_vector = vectorizer.transform(X_test)

# ===============================
# 4. Train Model
# ===============================

model = LogisticRegression(max_iter=1000)
model.fit(X_train_vector, y_train)

# ===============================
# 5. Evaluate Model
# ===============================

y_pred = model.predict(X_test_vector)

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:\n")
print(confusion_matrix(y_test, y_pred))

# ===============================
# 6. Save Model & Vectorizer
# ===============================

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("\nModel and Vectorizer saved successfully.")