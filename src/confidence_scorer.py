import numpy as np

class ConfidenceScorer:

    def softmax_confidence(self, logits):
        exp_logits = np.exp(logits - np.max(logits))
        probabilities = exp_logits / exp_logits.sum()
        return float(np.max(probabilities))

    def bayesian_confidence(self, predictions):
        return float(np.mean(predictions))

    def ensemble_confidence(self, scores):
        return float(np.mean(scores))

    def score(self, value, method="softmax"):
        if method == "softmax":
            return self.softmax_confidence(value)
        elif method == "bayesian":
            return self.bayesian_confidence(value)
        elif method == "ensemble":
            return self.ensemble_confidence(value)
        else:
            raise ValueError(f"Unknown method: {method}")
