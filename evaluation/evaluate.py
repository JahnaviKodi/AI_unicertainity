import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pipeline import Pipeline
from data.ground_truth import ground_truth

pipeline  = Pipeline()
decisions = ["ANSWER", "CLARIFY", "ABSTAIN", "ESCALATE"]

results   = []
correct   = 0
total     = len(ground_truth)

for item in ground_truth:
    query    = item["query"]
    expected = item["expected_decision"]
    category = item["risk_category"]
    result   = pipeline.run(query)
    actual   = result["decision"]
    passed   = actual == expected
    if passed:
        correct += 1
    results.append({
        "query":    query,
        "expected": expected,
        "actual":   actual,
        "passed":   passed,
        "category": category
    })

# ── OVERALL ACCURACY ─────────────────────────────────────
accuracy = (correct / total) * 100
print("\n========== EVALUATION RESULTS ==========\n")
for r in results:
    status = "PASS" if r["passed"] else "FAIL"
    print(f"[{status}] {r['query'][:55]}")
    print(f"       Expected: {r['expected']} | Actual: {r['actual']}\n")

print(f"========================================")
print(f"Total: {total} | Passed: {correct} | Failed: {total - correct}")
print(f"Accuracy: {accuracy:.2f}%")
print(f"========================================\n")

# ── CONFUSION MATRIX ─────────────────────────────────────
print("========== CONFUSION MATRIX ==========\n")
matrix = {d: {d2: 0 for d2 in decisions} for d in decisions}
for r in results:
    matrix[r["expected"]][r["actual"]] += 1

header = f"{'':12}" + "".join(f"{d:12}" for d in decisions)
print(header)
print("-" * (12 + 12 * len(decisions)))
for expected in decisions:
    row = f"{expected:12}" + "".join(f"{matrix[expected][actual]:12}" for actual in decisions)
    print(row)
print()

# ── PRECISION RECALL F1 ──────────────────────────────────
print("========== PRECISION / RECALL / F1 ==========\n")
print(f"{'Decision':12} {'Precision':12} {'Recall':12} {'F1 Score':12}")
print("-" * 48)

for d in decisions:
    tp = matrix[d][d]
    fp = sum(matrix[other][d] for other in decisions if other != d)
    fn = sum(matrix[d][other] for other in decisions if other != d)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall    = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1        = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    print(f"{d:12} {precision:12.2f} {recall:12.2f} {f1:12.2f}")

print()

# ── DOMAIN EVALUATION ────────────────────────────────────
print("========== DOMAIN EVALUATION ==========\n")
print(f"{'Category':12} {'Total':8} {'Correct':8} {'Accuracy':10}")
print("-" * 40)

categories = list(set(r["category"] for r in results))
for cat in categories:
    cat_results = [r for r in results if r["category"] == cat]
    cat_total   = len(cat_results)
    cat_correct = sum(1 for r in cat_results if r["passed"])
    cat_acc     = (cat_correct / cat_total) * 100 if cat_total > 0 else 0
    print(f"{cat:12} {cat_total:8} {cat_correct:8} {cat_acc:9.1f}%")

print()