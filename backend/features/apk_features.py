FEATURE_NAMES = [
    "ends_with_apk"
]

def extract(url):
    return {
        "ends_with_apk": 1 if url.lower().endswith(".apk") else 0
    }
