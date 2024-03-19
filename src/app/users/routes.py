"""Module for users related endpoints."""
from flask import Response, jsonify, make_response, request

from src.app.models.roles import RoleEnum
from src.app.services.user_service import UserService
from src.app.users import bp
from src.app.utils.password_hasher import PasswordHasher


@bp.route("/student")
def index() -> str:
    """Return example text for the users blueprint."""
    return "This is the users blueprint."


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
