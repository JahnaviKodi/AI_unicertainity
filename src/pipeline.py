import os
from dotenv import load_dotenv
import anthropic
from src.confidence_scorer import ConfidenceScorer
from src.boundary_detector import BoundaryDetector
from src.decision_engine import DecisionEngine
from src.response_generator import ResponseGenerator

load_dotenv()

class Pipeline:

    def __init__(self):
        self.scorer = ConfidenceScorer()
        self.detector = BoundaryDetector()
        self.engine = DecisionEngine()
        self.generator = ResponseGenerator()
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

    def get_real_answer(self, query):
        """
        Calls Claude API to get a real answer.
        """
        message = self.client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            messages=[
                {"role": "user", "content": query}
            ]
        )
        return message.content[0].text

    def run(self, query, logits=None, answer=None):
        """
        Full pipeline. Pass in a query and get back
        a final response with decision details.
        """

        # Step 1 - Classify the query
        boundary_result = self.detector.classify(query)

        # Step 2 - Score confidence
        if logits:
            confidence = self.scorer.score(logits, method="softmax")
        else:
            if boundary_result == "IN_DISTRIBUTION":
                confidence = 0.80
            elif boundary_result == "AMBIGUOUS":
                confidence = 0.60
            else:
                confidence = 0.40

        # Step 3 - Make decision
        decision = self.engine.decide(confidence, boundary_result)

        # Step 4 - Get real answer from Claude if decision is ANSWER
        if decision == "ANSWER":
            try:
                real_answer = self.get_real_answer(query)
            except Exception as e:
                real_answer = None
                print(f"API error: {e}")
        else:
            real_answer = None

        # Step 5 - Generate response
        response = self.generator.generate(decision, query, real_answer)

        return {
            "query": query,
            "boundary": boundary_result,
            "confidence": round(confidence, 4),
            "decision": decision,
            "response": response
        }