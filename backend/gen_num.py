import pandas as pd
from features.basic_features import extract, FEATURE_NAMES

# Example URLs
urls = [
    "https://www.google.com",
    "http://paypa1.com",
    "http://free-instagram-followers.net",
    "https://www.youtube.com"
]

labels = [1, 0, 0, 1]  # 1=legit, 0=fake

data = []
for url, label in zip(urls, labels):
    features = extract(url)
    features["label"] = label
    data.append(features)

df = pd.DataFrame(data)
df.to_csv("data/urls_numeric.csv", index=False)
print("✅ Numeric CSV saved as data/urls_numeric.csv")
