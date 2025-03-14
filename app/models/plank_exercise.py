from . import db

class PlankExercise(db.Model):
    __tablename__ = 'plank_exercises'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(), db.ForeignKey('users.id'), unique=True, nullable=False)
    correct = db.Column(db.Integer, default=0)
    incorrect = db.Column(db.Integer, default=0)
    feedback = db.Column(db.JSON, default=lambda: {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0})

    def __init__(self, user_id, **kwargs):
        super(PlankExercise, self).__init__(user_id=user_id, correct=0, incorrect=0, feedback={"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0}, **kwargs)
