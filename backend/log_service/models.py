from datetime import datetime
from database import db

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
