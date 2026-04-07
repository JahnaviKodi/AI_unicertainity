import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pipeline import Pipeline
from src.confidence_scorer import ConfidenceScorer
from src.boundary_detector import BoundaryDetector
from src.decision_engine import DecisionEngine

pipeline = Pipeline()
scorer = ConfidenceScorer()
detector = BoundaryDetector()
engine = DecisionEngine()

# ── Confidence Scorer Tests ──────────────────────────────

def test_softmax_high_confidence():
    score = scorer.score([5.0, 1.0, 0.1], "softmax")
    assert score > 0.75, "Expected high confidence"

def test_softmax_low_confidence():
    score = scorer.score([1.0, 1.0, 1.0], "softmax")
    assert score < 0.75, "Expected low confidence for equal logits"

def test_bayesian_confidence():
    score = scorer.score([0.8, 0.7, 0.9], "bayesian")
    assert 0.7 < score < 1.0

def test_ensemble_confidence():
    score = scorer.score([0.6, 0.7, 0.8], "ensemble")
    assert round(score, 2) == 0.70

# ── Boundary Detector Tests ──────────────────────────────

def test_in_distribution():
    result = detector.classify("How does machine learning work?")
    assert result == "IN_DISTRIBUTION"

def test_high_risk_medical():
    result = detector.classify("What medicine should I take?")
    assert result == "HIGH_RISK"

def test_high_risk_legal():
    result = detector.classify("How do I win my lawsuit?")
    assert result == "HIGH_RISK"

def test_ambiguous_short():
    result = detector.classify("What?")
    assert result == "AMBIGUOUS"

def test_out_of_distribution():
    result = detector.classify("Tell me my astrology future")
    assert result == "OUT_OF_DISTRIBUTION"

# ── Decision Engine Tests ────────────────────────────────

def test_decision_answer():
    result = engine.decide(0.85, "IN_DISTRIBUTION")
    assert result == "ANSWER"

def test_decision_clarify():
    result = engine.decide(0.60, "AMBIGUOUS")
    assert result == "CLARIFY"

def test_decision_abstain():
    result = engine.decide(0.30, "IN_DISTRIBUTION")
    assert result == "ABSTAIN"

def test_decision_escalate():
    result = engine.decide(0.90, "HIGH_RISK")
    assert result == "ESCALATE"

# ── Full Pipeline Tests ──────────────────────────────────

def test_pipeline_answer():
    result = pipeline.run("How does machine learning work?")
    assert result["decision"] == "ANSWER"

def test_pipeline_escalate():
    result = pipeline.run("What medicine should I take for fever?")
    assert result["decision"] == "ESCALATE"

def test_pipeline_abstain():
    result = pipeline.run("Tell me my fortune with astrology")
    assert result["decision"] == "ABSTAIN"

def test_pipeline_clarify():
    result = pipeline.run("Maybe?")
    assert result["decision"] == "CLARIFY" 
