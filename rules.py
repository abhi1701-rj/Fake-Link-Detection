import re
import urllib.parse

SUSPICIOUS_KEYWORDS = [
    "login", "verify", "secure", "update",
    "account", "bank", "confirm", "free", "gift"
]

def has_ip_address(url):
    return bool(re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', url))

def url_length_check(url):
    return len(url) > 75

def count_subdomains(url):
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc
    return domain.count('.') > 3

def contains_unicode(url):
    try:
        url.encode("ascii")
        return False
    except UnicodeEncodeError:
        return True

def contains_suspicious_keywords(url):
    return any(word in url.lower() for word in SUSPICIOUS_KEYWORDS)

def rule_based_check(url):
    flags = []

    if has_ip_address(url):
        flags.append("IP address in URL")

    if url_length_check(url):
        flags.append("Very long URL")

    if count_subdomains(url):
        flags.append("Too many subdomains")

    if contains_unicode(url):
        flags.append("Unicode / homograph attack")

    if contains_suspicious_keywords(url):
        flags.append("Suspicious keywords")

    return flags
