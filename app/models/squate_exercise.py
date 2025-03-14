from . import db

class SquatExercise(db.Model):
    __tablename__ = 'squat_exercises'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(), db.ForeignKey('users.id'), unique=True, nullable=False)
    correct = db.Column(db.Integer, default=0)
    incorrect = db.Column(db.Integer, default=0)
    feedback = db.Column(db.JSON, default=lambda: {"0": 0, "1": 0, "2": 0, "3": 0})
    duration = db.Column(db.Integer)  # This could also have a default if necessary

    def __init__(self, user_id, **kwargs):
        super(SquatExercise, self).__init__(user_id=user_id, correct=0, incorrect=0, feedback={"0": 0, "1": 0, "2": 0, "3": 0}, **kwargs)
