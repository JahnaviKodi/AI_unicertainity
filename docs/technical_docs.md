# Technical Documentation

## Architecture
Input Query
   → BoundaryDetector.classify()
   → ConfidenceScorer.score()
   → DecisionEngine.decide()
   → ResponseGenerator.generate()
   → Final Response

## Modules

### ConfidenceScorer
- score(value, method) → float (0 to 1)
- Methods: softmax, bayesian, ensemble

### BoundaryDetector
- classify(text) → IN_DISTRIBUTION | OUT_OF_DISTRIBUTION | AMBIGUOUS | HIGH_RISK

### DecisionEngine
- decide(confidence, boundary) → ANSWER | CLARIFY | ABSTAIN | ESCALATE
- update_thresholds(answer, clarify) → updates decision thresholds

### ResponseGenerator
- generate(decision, query, answer) → string response

### Pipeline
- run(query, logits, answer) → dict with full result details

## Configuration
- Answer threshold: 0.75 (adjustable via update_thresholds)
- Clarify threshold: 0.50 (adjustable via update_thresholds)

## Dependencies
- numpy
- transformers
- torch
- scikit-learn
- pytest

## Known Limitations
- Keyword based boundary detection is basic
- Needs real model logits for production use
- Thresholds need tuning on real world data 
