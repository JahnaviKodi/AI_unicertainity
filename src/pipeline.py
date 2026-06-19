import os
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
from dotenv import load_dotenv
from groq import Groq
from src.confidence_scorer import ConfidenceScorer
from src.boundary_detector import BoundaryDetector
from src.decision_engine import DecisionEngine
from src.response_generator import ResponseGenerator
logger = logging.getLogger(__name__)
load_dotenv()

class Pipeline:

    def __init__(self):
        self.scorer    = ConfidenceScorer()
        self.detector  = BoundaryDetector()
        self.engine    = DecisionEngine()
        self.generator = ResponseGenerator()
        self.client    = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

    def get_real_answer(self, query):
        """
        Calls Groq API to get a real answer.
        Uses Llama 3 model — completely free.
        """
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Answer clearly and concisely."
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            max_tokens=500
        )
        return response.choices[0].message.content

    def run(self, query, logits=None, answer=None):

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

        # Step 4 - Get real answer from Groq if decision is ANSWER
        if decision == "ANSWER":
            try:
                real_answer = self.get_real_answer(query)
            except Exception as e:
                real_answer = None
                logger.error(f"Groq API error: {e}")
        else:
            real_answer = None

        # Step 5 - Generate response
        response = self.generator.generate(decision, query, real_answer)

        return {
            "query":      query,
            "boundary":   boundary_result,
            "confidence": round(confidence, 4),
            "decision":   decision,
            "response":   response
        }