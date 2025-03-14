from flask import Blueprint, request, jsonify
from app.models.user import User
from app.models.plank_exercise import PlankExercise
from app.models.squate_exercise import SquatExercise
from app.models import db
from uuid import uuid4
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    current_user,
    get_jwt_identity,
)
from app.models.tokenblocklist import TokenBlocklist

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    gender = data.get('gender')
    age = data.get('age')

    try:
        height = float(data.get('height', 0))
        weight = float(data.get('weight', 0))
    except ValueError:
        return jsonify({'error': 'Invalid data format for height or weight'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 409
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 409

    userid = str(uuid4())
    user = User(id=userid, username=username, email=email, password=password, gender=gender, age=age, height=height, weight=weight)
    user.set_password(password)

    # Add and commit user to ensure it exists in the database before adding exercises
    db.session.add(user)
    db.session.commit()  # Commit here to ensure user is actually saved and can be referenced

    # Now add exercises
    plank_exercise = PlankExercise(user_id=userid)
    squat_exercise = SquatExercise(user_id=userid)

    db.session.add(plank_exercise)
    db.session.add(squat_exercise)
    db.session.commit()

    return jsonify({'message': 'User registered successfully', 'user_id': userid}), 201


@auth_blueprint.post("/login")
def login_user():
    data = request.get_json()

    user = User.get_user_by_username(username=data.get("username"))

    if user and (user.check_password(password=data.get("password"))):
        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)

        return (
            jsonify(
                {
                    "message": "Logged In ",
                    "tokens": {"access": access_token, "refresh": refresh_token},
                }
            ),
            200,
        )

    return jsonify({"error": "Invalid username or password"}), 400


@auth_blueprint.get("/whoami")
@jwt_required()
def whoami():
    return jsonify(
        {
            "message": "message",
            "user_details": {
                "username": current_user.username,
                "email": current_user.email,
            },
        }
    )

@auth_blueprint.post("/refresh")
@jwt_required(refresh=True)
def refresh_access():
    identity = get_jwt_identity()

    new_access_token = create_access_token(identity=identity)

    return jsonify({"access_token": new_access_token})


@auth_blueprint.get('/logout')
@jwt_required(verify_type=False) 
def logout_user():
    jwt = get_jwt()

    jti = jwt['jti']
    token_type = jwt['type']

    token_b = TokenBlocklist(jti=jti)

    token_b.save()

    return jsonify({"message": f"{token_type} token revoked successfully"}) , 200






