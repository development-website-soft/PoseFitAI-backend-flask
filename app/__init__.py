from flask import Flask, jsonify
from .models import db, migrate, jwt
from config import Config
from .routes.auth_routes import auth_blueprint
from .routes.user_routes import users_blueprint
from .routes.session_routes import session_blueprint
from .routes.plank_routes import plank_blueprint
from .routes.squate_routes import squat_blueprint
from app.models.user import User
from app.models.tokenblocklist import TokenBlocklist
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, resources={r"/*": {"origins": "*"}})

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    @app.route('/')
    def home():
        return 'Hello, Flask is running!'

    # Register blueprints for routes
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(users_blueprint, url_prefix='/user')
    app.register_blueprint(session_blueprint, url_prefix='/session')
    app.register_blueprint(plank_blueprint, url_prefix='/plank')
    app.register_blueprint(squat_blueprint, url_prefix='/squat')

     # load user
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_headers, jwt_data):
        identity = jwt_data["sub"]

        return User.query.filter_by(username=identity).one_or_none()

    # additional claims

    @jwt.additional_claims_loader
    def make_additional_claims(identity):
        if identity == "janedoe123":
            return {"is_staff": True}
        return {"is_staff": False}

    # jwt error handlers

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({"message": "Token has expired", "error": "token_expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "message": "Request doesnt contain valid token",
                    "error": "authorization_header",
                }
            ),
            401,
        )
    
    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(jwt_header,jwt_data):
        jti = jwt_data['jti']

        token = db.session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).scalar()

        return token is not None

    return app
