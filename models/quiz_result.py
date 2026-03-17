from database.db import db

class QuizResult(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, nullable=False)

    level = db.Column(db.String(50), nullable=False)

    score = db.Column(db.Integer, nullable=False)

    total = db.Column(db.Integer, nullable=False)

    percentage = db.Column(db.Float, nullable=False)