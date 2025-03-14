from flask import Blueprint, jsonify
from app.models.user import User
from app.models import db
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity

users_blueprint = Blueprint('user', __name__)

@users_blueprint.route('/all', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    users_list = [{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'weight': user.weight,
        'height': user.height,
        'gender': user.gender,
        'age': user.age,
    } for user in users]

    return jsonify(users_list), 200

@users_blueprint.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    id = current_user.id
    user = User.query.get(id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'weight': user.weight,
        'height': user.height,
        'gender': user.gender,
        'age': user.age,
    }), 200
