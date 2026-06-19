import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import matplotlib.pyplot as plt
import numpy as np
from src.pipeline import Pipeline
from data.ground_truth import ground_truth

pipeline = Pipeline()

confidence_scores = []
correct_flags     = []

for item in ground_truth:
    result  = pipeline.run(item["query"])
    correct = result["decision"] == item["expected_decision"]
    confidence_scores.append(result["confidence"])
    correct_flags.append(int(correct))

# ── BIN DATA ─────────────────────────────────────────────
bins       = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
bin_labels = ["0.0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1.0"]
bin_conf   = []
bin_acc    = []

for i in range(len(bins) - 1):
    low, high = bins[i], bins[i+1]
    indices   = [j for j, c in enumerate(confidence_scores) if low <= c < high]
    if indices:
        avg_conf = np.mean([confidence_scores[j] for j in indices])
        avg_acc  = np.mean([correct_flags[j]     for j in indices])
    else:
        avg_conf = (low + high) / 2
        avg_acc  = 0.0
    bin_conf.append(avg_conf)
    bin_acc.append(avg_acc)

# ── PLOT ─────────────────────────────────────────────────
plt.figure(figsize=(8, 6))
plt.plot([0, 1], [0, 1], "k--", label="Perfect Calibration")
plt.plot(bin_conf, bin_acc, "bo-", linewidth=2, markersize=8, label="System Calibration")
plt.fill_between(bin_conf, bin_acc, bin_conf,
                 alpha=0.2, color="red", label="Calibration Gap")

plt.xlabel("Mean Confidence Score")
plt.ylabel("Actual Accuracy")
plt.title("Confidence Calibration Graph")
plt.legend()
plt.grid(True, alpha=0.3)
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig("evaluation/calibration_graph.png", dpi=150)
plt.show()
print("Calibration graph saved to evaluation/calibration_graph.png") 
