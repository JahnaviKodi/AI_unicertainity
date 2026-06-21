class BoundaryDetector:
    def __init__(self):
        # Keywords that indicate ambiguous queries
        self.ambiguous_keywords = [
            "maybe", "not sure", "kind of", "sort of",
            "huh", "idk", "unclear", "tell me something",
            "can you explain", "explain anything"
        ]

        # Keywords that indicate high-risk domains
        self.high_risk_keywords = [
            # Medical
            "medicine", "medical", "medication", "drug", "drugs",
            "dose", "dosage", "symptom", "symptoms", "diagnose",
            "diagnosis", "disease", "cancer", "surgery", "treatment",
            "doctor", "hospital", "prescription", "pill", "pills",
            "tablet", "injection", "vaccine", "virus", "infection",
            "pain", "chest pain", "fever", "bleeding", "overdose",
            "mental health", "depression", "anxiety", "suicide",
            "pregnant", "pregnancy", "allergy", "allergic",
            "headache", "nausea", "vomiting", "diabetes", "stroke",
            "heart attack", "blood pressure", "cholesterol", "therapy",
            "psychiatrist", "psychologist", "rehab", "addiction",
            # Legal
            "lawyer", "legal", "lawsuit", "sue", "court", "attorney",
            "crime", "criminal", "murder", "kill", "weapon", "gun",
            "illegal", "arrest", "police", "jail", "prison", "theft",
            "fraud", "abuse", "assault", "trafficking", "hack",
            "employer", "contract", "binding", "rights", "bail",
            "parole", "conviction", "sentence", "verdict", "witness",
            "evidence", "defend", "prosecute", "charge", "offence",
            "rape", "kidnap", "robbery", "burglary", "extortion",
            "bribe", "corruption", "smuggle", "terrorist", "bomb",
            "explosive", "poison", "stab", "shoot", "threaten",
            # Financial
            "financial", "finance", "invest", "investment",
            "crypto", "cryptocurrency", "bitcoin", "ethereum",
            "stocks", "shares", "trading", "tax", "insurance",
            "loan", "debt", "bankruptcy", "mortgage", "pension",
            "forex", "hedge fund", "derivatives", "portfolio",
            "dividend", "interest rate", "inflation", "recession",
            "money laundering", "ponzi", "scam", "pyramid scheme"
        ]

        # Keywords that are clearly out of domain
        self.out_of_domain_keywords = [
            "lottery", "magic", "supernatural", "alien",
            "fortune telling", "astrology", "horoscope",
            "tarot", "psychic", "crystal ball", "lucky numbers",
            "future", "predict my", "fate", "destiny", "spell",
            "ghost", "demon", "witch", "wizard", "curse",
            "jinx", "voodoo", "occult", "spirit", "haunted",
            "ufo", "extraterrestrial", "mythology", "prophecy"
        ]

        # Vague words that often indicate missing context
        self.vague_terms = [
            "it",
            "this",
            "that",
            "thing",
            "stuff",
        ]

    def detect_ambiguity(self, text):
        """
        Returns True if the query seems ambiguous or vague.
        """
        text_lower = text.lower().strip()
        words = text_lower.split()
        words = [word.strip("?!.,;:") for word in words]

        # Very short queries are usually ambiguous
        if len(words) <= 2:
            return True

        # Ambiguous phrases
        for phrase in self.ambiguous_keywords:
            if phrase in text_lower:
                return True

        # Vague pronoun-based short queries
        if len(words) <= 4:
            for word in self.vague_terms:
                if word in words:
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
        Returns True if the query is in a high-risk domain.
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

        HIGH_RISK is checked first to ensure medical,
        legal, financial and crime queries are always
        escalated before any other classification.
        """
        if self.is_high_risk(text):
            return "HIGH_RISK"
        elif self.is_out_of_distribution(text):
            return "OUT_OF_DISTRIBUTION"
        elif self.detect_ambiguity(text):
            return "AMBIGUOUS"
        else:
            return "IN_DISTRIBUTION"