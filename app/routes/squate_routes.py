from flask import Blueprint, request, jsonify
from app.models import db
from app.models.squate_exercise import SquatExercise
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy.orm.attributes import flag_modified

squat_blueprint = Blueprint('squat', __name__)

@squat_blueprint.route('/add', methods=['POST'])
@jwt_required()
def add_or_update_squat():
    data = request.get_json()

    correct = data.get('correct', 0)
    incorrect = data.get('incorrect', 0)
    new_feedback = data.get('feedback', {})

    # Query the existing squat exercise for the current user
    existing_squat = SquatExercise.query.filter_by(user_id=current_user.id).first()

    if existing_squat:
        # Update the existing squat exercise
        existing_squat.correct += correct
        existing_squat.incorrect += incorrect

        # Merge the new feedback with the existing feedback
        for key, value in new_feedback.items():
            if key in existing_squat.feedback:
                existing_squat.feedback[key] += value
            else:
                existing_squat.feedback[key] = value

        # Mark the feedback as modified
        flag_modified(existing_squat, 'feedback')

        # Commit the changes to the database
        db.session.commit()

        return jsonify({'message': 'Squat exercise updated', 'id': existing_squat.id}), 200
    else:
        # Create a new squat exercise
        new_squat = SquatExercise(
            user_id=current_user.id,
            correct=correct,
            incorrect=incorrect,
            feedback=new_feedback
        )
        db.session.add(new_squat)
        db.session.commit()

        return jsonify({'message': 'Squat exercise added', 'id': new_squat.id}), 201

@squat_blueprint.route('/get', methods=['GET'])
@jwt_required()
def get_squat():
    squat = SquatExercise.query.filter_by(user_id=current_user.id).first()
    if squat:
        return jsonify({
            'correct': squat.correct,
            'incorrect': squat.incorrect,
            'feedback': squat.feedback
        }), 200
    else:
        return jsonify({'message': 'Squat exercise not found'}), 404
