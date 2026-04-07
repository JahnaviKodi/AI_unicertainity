class ResponseGenerator:

    def generate(self, decision, query, answer=None):
        """
        Main entry point. Takes decision and query
        and returns a user friendly response.
        """

        if decision == "ANSWER":
            return self._answer_response(answer)

        elif decision == "CLARIFY":
            return self._clarify_response(query)

        elif decision == "ABSTAIN":
            return self._abstain_response()

        elif decision == "ESCALATE":
            return self._escalate_response()

        else:
            return "I am unable to process this request."

    def _answer_response(self, answer):
        if answer:
            return f"Based on my knowledge: {answer}"
        return "I have an answer but it was not provided."

    def _clarify_response(self, query):
        return (
            f"I want to make sure I understand your question correctly. "
            f"Could you provide more details about: '{query}'?"
        )

    def _abstain_response(self):
        return (
            "I don't have enough reliable information to answer this "
            "confidently. I'd rather not guess than give you wrong information."
        )

    def _escalate_response(self):
        return (
            "This question involves a sensitive or high risk domain such as "
            "medical, legal, or financial advice. I recommend consulting a "
            "qualified expert for accurate guidance."
        ) 
