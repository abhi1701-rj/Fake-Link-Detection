import re
from urllib.parse import urlparse

def extract_features(url):
    features = []

    features.append(len(url))                     # URL length
    features.append(url.count('.'))               # Dot count
    features.append(url.count('-'))               # Hyphen count
    features.append(1 if "https" in url else 0)   # HTTPS
    features.append(1 if "@" in url else 0)        # @ symbol
    features.append(1 if "//" in url else 0)       # Redirect

    return features
