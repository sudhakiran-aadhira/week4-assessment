
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent

def classify(ticket, version):
    ticket = ticket.lower()

    billing_words = [
        "charge", "payment", "invoice", "refund",
        "subscription", "bill", "credit card"
    ]

    technical_words = [
        "crash", "error", "slow", "bug",
        "blank screen", "application", "app", "website"
    ]

    account_words = [
        "password", "email", "profile",
        "account", "registered"
    ]

    if version == "v1":
        # Basic rules for the first prompt
        if any(word in ticket for word in billing_words):
            return "Billing"
        if any(word in ticket for word in technical_words):
            return "Technical"
        return "Account"

    # Improved rules for the second prompt
    if any(word in ticket for word in billing_words):
        return "Billing"

    if any(word in ticket for word in technical_words):
        return "Technical"

    if any(word in ticket for word in account_words):
        return "Account"

    return "Account"


def run_eval(version):
    dataset_path = BASE_DIR / "golden.jsonl"

    with open(dataset_path, encoding="utf-8") as file:
        tickets = [json.loads(line) for line in file if line.strip()]

    correct = 0

    for item in tickets:
        predicted = classify(item["ticket"], version)
        expected = item["category"]

        if predicted == expected:
            correct += 1

        print(
            f"Expected: {expected} | "
            f"Predicted: {predicted}"
        )

    total = len(tickets)
    accuracy = correct / total * 100

    print(f"\n{version}: {correct}/{total} ({accuracy:.0f}%)")
    return accuracy


if __name__ == "__main__":
    v1_accuracy = run_eval("v1")
    v2_accuracy = run_eval("v2")

    print("\nAccuracy comparison")
    print(f"V1: {v1_accuracy:.0f}%")
    print(f"V2: {v2_accuracy:.0f}%")
    print(f"Difference: {v2_accuracy - v1_accuracy:+.0f} percentage points")