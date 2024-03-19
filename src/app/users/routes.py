"""Module for users related endpoints."""
from flask import Response, jsonify, make_response, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from src.app.models.users import Users
from src.app.users import bp
from src.app.utils.password_hasher import PasswordHasher


@bp.route("/student")
def index() -> str:
    """Return example text for the users blueprint."""
    return "This is the users blueprint."


@bp.route("/users/get_current_user", methods=["GET"])
@jwt_required()
def get_current_user() -> Response:
    """Return the user information."""
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user)


@bp.route("/users/login", methods=["POST"])
def login() -> Response:
    """Generate a JWT token for the user."""
    try:
        username = request.json["username"]
        password = request.json["password"]
    except KeyError:
        response = {"message": "Invalid request"}
        return make_response(jsonify(response), 400)

    user = Users.query.filter_by(username=username).first()

    if user is None:
        response = {"message": "User not found"}
        return make_response(jsonify(response), 404)
    elif PasswordHasher.verify_password(password, user.password) is False:
        response = {"message": "Invalid password"}
        return make_response(jsonify(response), 401)

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)
