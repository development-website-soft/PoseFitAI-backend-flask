from . import db

class SessionHistory(db.Model):
    __tablename__ = 'session_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(), db.ForeignKey('users.id'), nullable=False)
    exercise_name = db.Column(db.String(100))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    correct = db.Column(db.Integer, default=0)
    incorrect = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=True)
    feedback = db.Column(db.JSON, default=lambda: {})