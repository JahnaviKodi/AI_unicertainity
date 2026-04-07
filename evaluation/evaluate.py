import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pipeline import Pipeline
from data.ground_truth import ground_truth

pipeline = Pipeline()

correct = 0
total = len(ground_truth)
results = []

for item in ground_truth:
    query = item["query"]
    expected = item["expected_decision"]

    result = pipeline.run(query)
    actual = result["decision"]
    passed = actual == expected

    if passed:
        correct += 1

    results.append({
        "query": query,
        "expected": expected,
        "actual": actual,
        "passed": passed
    })

# Print results
print("\n========== EVALUATION RESULTS ==========\n")
for r in results:
    status = "PASS" if r["passed"] else "FAIL"
    print(f"[{status}] Query: {r['query'][:50]}")
    print(f"       Expected: {r['expected']} | Actual: {r['actual']}\n")

accuracy = (correct / total) * 100
print(f"========================================")
print(f"Total: {total} | Passed: {correct} | Failed: {total - correct}")
print(f"Accuracy: {accuracy:.2f}%")
print(f"========================================\n") 
