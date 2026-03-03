import csv

real_domains = [
    "google", "youtube", "facebook", "amazon", "microsoft",
    "apple", "netflix", "linkedin", "instagram", "twitter",
    "wikipedia", "github", "reddit", "paypal", "flipkart",
    "snapdeal", "icicibank", "hdfcbank", "axisbank", "sbi"
]

fake_keywords = [
    "secure", "login", "verify", "update", "alert",
    "account", "banking", "wallet", "support", "confirm",
    "free", "bonus", "lottery", "crypto", "offer"
]

with open("phishing_dataset.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["url", "label"])

    # 250 REAL URLs
    for i in range(250):
        domain = real_domains[i % len(real_domains)]
        writer.writerow([f"http://{domain}{i}.com", "REAL"])

    # 250 FAKE URLs
    for i in range(250):
        keyword = fake_keywords[i % len(fake_keywords)]
        writer.writerow([f"http://{keyword}-account{i}-security.xyz", "FAKE"])

print("500 URL dataset generated successfully.")