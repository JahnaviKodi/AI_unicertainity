from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class QueryLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.Text, nullable=False)
    decision = db.Column(db.String(20), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    boundary = db.Column(db.String(30), nullable=False)
    response = db.Column(db.Text, nullable=False)
    response_time = db.Column(db.Float, nullable=False)
    feedback = db.Column(db.String(10), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "query": self.query,
            "decision": self.decision,
            "confidence": self.confidence,
            "boundary": self.boundary,
            "response": self.response,
            "response_time": self.response_time,
            "feedback": self.feedback,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }