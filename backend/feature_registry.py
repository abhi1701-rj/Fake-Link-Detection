from features.basic_features import extract as basic_extract, FEATURE_NAMES as BASIC
from features.apk_features import extract as apk_extract, FEATURE_NAMES as APK

FEATURE_SETS = {
    "basic": {
        "features": BASIC,
        "extract": basic_extract,
        "model": "models/rf_basic.pkl"
    },
    "apk": {
        "features": APK,
        "extract": apk_extract,
        "model": None  # rule-based only
    }
}
