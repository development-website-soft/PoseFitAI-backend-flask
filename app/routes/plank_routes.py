from flask import Blueprint, request, jsonify
from app.models import db
from app.models.plank_exercise import PlankExercise
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy.orm.attributes import flag_modified

plank_blueprint = Blueprint('plank', __name__)

@plank_blueprint.route('/add', methods=['POST'])
@jwt_required()
def add_or_update_plank():
    data = request.get_json()

    # Extract the values from the request data
    correct = data.get('correct', 0)
    incorrect = data.get('incorrect', 0)
    new_feedback = data.get('feedback', {})

    # Query the existing plank exercise for the current user
    existing_plank = PlankExercise.query.filter_by(
        user_id=current_user.id
    ).first()

    if existing_plank:
        # Update the existing plank exercise counts
        existing_plank.correct += correct
        existing_plank.incorrect += incorrect

        # Merge the new feedback counts with the existing feedback
        for key, value in new_feedback.items():
            if key in existing_plank.feedback:
                existing_plank.feedback[key] += value
            else:
                existing_plank.feedback[key] = value

        # Explicitly mark the feedback field as modified
        flag_modified(existing_plank, 'feedback')

        # Commit the changes to the database
        db.session.commit()

        return jsonify({'message': 'Plank exercise updated', 'id': existing_plank.id}), 200
    else:
        # Create a new plank exercise
        new_plank = PlankExercise(
            user_id=current_user.id,
            correct=correct,
            incorrect=incorrect,
            feedback=new_feedback
        )
        db.session.add(new_plank)
        db.session.commit()

        return jsonify({'message': 'Plank exercise added', 'id': new_plank.id}), 201

@plank_blueprint.route('/get', methods=['GET'])
@jwt_required()
def get_plank():
    plank = PlankExercise.query.filter_by(user_id=current_user.id).first()
    if plank:
        return jsonify({
            'correct': plank.correct,
            'incorrect': plank.incorrect,
            'feedback': plank.feedback
        }), 200
    else:
        return jsonify({'message': 'Plank exercise not found'}), 404
