import requests
import time
URL = "http://127.0.0.1:8000/ask"
tests = [
    # 6 answerable questions
    ("How do I reset my password?", True),
    ("Where can I update my email address?", True),
    ("Where can I view invoices?", True),
    ("What if payment is deducted twice?", True),
    ("How can I track my order?", True),
    ("What should I do if the mobile app crashes?", True),
    # 4 unanswerable questions
    ("What is the CEO's birthday?", False),
    ("What is the company office address?", False),
    ("How many employees does the company have?", False),
    ("What is the CEO's phone number?", False),
]
passed = 0
failed = 0
print("\nRAG TEST RESULTS\n")
for number, (question, answerable) in enumerate(tests, start=1):
    start = time.time()
    try:
        response = requests.post(
            URL,
            json={"question": question},
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        answer = result.get("answer", "")
        sources = result.get("sources", [])
        if answerable:
            success = (
                answer != "I don't know."
                and len(sources) > 0
            )
        else:
            success = answer == "I don't know."
        elapsed = time.time() - start
        if success:
            passed += 1
            status = "PASS"
        else:
            failed += 1
            status = "FAIL"
        print(f"\nTest {number}: {status}")
        print(f"Question: {question}")
        print(f"Answer: {answer}")
        print(f"Sources: {sources}")
        print(f"Response time: {elapsed:.2f} seconds")
    except requests.RequestException as error:
        failed += 1
        print(f"\nTest {number}: ERROR")
        print(error)
print("\nSUMMARY")
print(f"Passed: {passed}/10")
print(f"Failed: {failed}/10")