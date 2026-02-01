# backend/features/basic_features.py

from urllib.parse import urlparse

FEATURE_NAMES = [
    "url_length",
    "has_https",
    "has_ip",
    "has_at",
    "dot_count",
    "digit_count",
    "hyphen_count",
    "subdomain_count"
]

def extract(url):
    features = {}
    features["url_length"] = len(url)
    features["has_https"] = 1 if url.startswith("https") else 0
    features["has_ip"] = 1 if any(char.isdigit() for char in url.split("/")[2] if char.isdigit()) else 0
    features["has_at"] = 1 if "@" in url else 0
    features["dot_count"] = url.count(".")
    features["digit_count"] = sum(c.isdigit() for c in url)
    features["hyphen_count"] = url.count("-")
    parsed = urlparse(url)
    features["subdomain_count"] = parsed.netloc.count(".") - 1
    return features
