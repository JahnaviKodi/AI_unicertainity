class BoundaryDetector:

    def __init__(self):
        # Keywords that indicate ambiguous queries
        self.ambiguous_keywords = [
            "maybe", "not sure", "kind of", "sort of",
            "what is", "huh", "idk", "unclear"
        ]

        # Keywords that indicate high risk domains
        self.high_risk_keywords = [
            "medicine", "medical", "legal", "lawyer",
            "financial", "finance", "surgery", "drug",
            "lawsuit", "investment", "diagnosis"
        ]

        # Keywords that are clearly out of domain
        self.out_of_domain_keywords = [
            "lottery", "magic", "supernatural", "alien",
            "fortune telling", "astrology"
        ]

    def detect_ambiguity(self, text):
        """
        Returns True if the query seems ambiguous or vague.
        """
        text_lower = text.lower()

        # Too short to be a proper question
        if len(text.split()) < 3:
            return True

        # Contains ambiguous words
        for word in self.ambiguous_keywords:
            if word in text_lower:
                return True

        return False

    def is_out_of_distribution(self, text):
        """
        Returns True if the query is outside the known domain.
        """
        text_lower = text.lower()

        for word in self.out_of_domain_keywords:
            if word in text_lower:
                return True

        return False

    def is_high_risk(self, text):
        """
        Returns True if the query is in a high risk domain.
        """
        text_lower = text.lower()

        for word in self.high_risk_keywords:
            if word in text_lower:
                return True

        return False

    def classify(self, text):
        """
        Main entry point. Returns one of:
        IN_DISTRIBUTION, OUT_OF_DISTRIBUTION,
        AMBIGUOUS, HIGH_RISK
        """
        if self.is_out_of_distribution(text):
            return "OUT_OF_DISTRIBUTION"

        elif self.is_high_risk(text):
            return "HIGH_RISK"

        elif self.detect_ambiguity(text):
            return "AMBIGUOUS"

        else:
            return "IN_DISTRIBUTION"