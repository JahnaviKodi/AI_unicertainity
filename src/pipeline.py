from src.confidence_scorer import ConfidenceScorer
from src.boundary_detector import BoundaryDetector
from src.decision_engine import DecisionEngine
from src.response_generator import ResponseGenerator


class Pipeline:
    def __init__(self):
        self.scorer = ConfidenceScorer()
        self.detector = BoundaryDetector()
        self.engine = DecisionEngine()
        self.generator = ResponseGenerator()

    def run(self, query, logits=None, answer=None):
        """
        Full pipeline. Pass in a query and get back
        a final response with decision details.
        """

        # Step 1 - Classify the query
        boundary_result = self.detector.classify(query)

        # Step 2 - Score confidence
        if logits is not None:
            confidence = self.scorer.score(logits, method="softmax")
        else:
            # Default confidence if no logits provided
            if boundary_result == "IN_DISTRIBUTION":
                confidence = 0.80
            elif boundary_result == "AMBIGUOUS":
                confidence = 0.60
            else:
                confidence = 0.40

        # Step 3 - Make decision
        decision = self.engine.decide(confidence, boundary_result)

        # Step 4 - Generate response
        response = self.generator.generate(decision, query, answer)

        # Return full details
        return {
            "query": query,
            "boundary": boundary_result,
            "confidence": round(confidence, 4),
            "decision": decision,
            "response": response,
        }