class DecisionEngine:

    def __init__(self):
        # Confidence thresholds
        self.answer_threshold = 0.75
        self.clarify_threshold = 0.50

    def decide(self, confidence_score, boundary_result):
        """
        Main entry point. Takes confidence score and
        boundary result and returns a decision.

        Returns one of:
        ANSWER, CLARIFY, ABSTAIN, ESCALATE
        """

        # If high risk domain always escalate
        if boundary_result == "HIGH_RISK":
            return "ESCALATE"

        # If out of distribution always abstain
        if boundary_result == "OUT_OF_DISTRIBUTION":
            return "ABSTAIN"

        # If ambiguous and somewhat confident ask to clarify
        if boundary_result == "AMBIGUOUS":
            if confidence_score >= self.clarify_threshold:
                return "CLARIFY"
            else:
                return "ABSTAIN"

        # If in distribution apply confidence thresholds
        if boundary_result == "IN_DISTRIBUTION":
            if confidence_score >= self.answer_threshold:
                return "ANSWER"
            elif confidence_score >= self.clarify_threshold:
                return "CLARIFY"
            else:
                return "ABSTAIN"

        # Default fallback
        return "ABSTAIN"

    def update_thresholds(self, answer_threshold, clarify_threshold):
        """
        Use this during tuning phase to adjust thresholds
        based on evaluation results.
        """
        self.answer_threshold = answer_threshold
        self.clarify_threshold = clarify_threshold
        print(f"Thresholds updated — Answer: {answer_threshold}, Clarify: {clarify_threshold}")
