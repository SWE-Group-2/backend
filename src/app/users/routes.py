"""Module for users related endpoints."""
from flask import Response, jsonify, make_response, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from src.app.models.roles import RoleEnum
from src.app.models.users import Users
from src.app.services.user_service import UserService
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


@bp.route("/users/register", methods=["POST"])
def register() -> Response:
    """Register a new user."""
    try:
        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        username = request.json["username"]
        password = request.json["password"]
    except KeyError:
        response = {"message": "Invalid request body"}
        return make_response(jsonify(response), 400)

    if UserService.get_user_by_username(username=username):
        response = {"message": "Username already exists"}
        return make_response(jsonify(response), 409)

    UserService.create_user(
        first_name=first_name,
        last_name=last_name,
        username=username,
        password=PasswordHasher.hash_password(password=password),
        role_id=RoleEnum.student.value,
    )

    response = {"message": "User created successfully"}
    return make_response(jsonify(response), 201)
