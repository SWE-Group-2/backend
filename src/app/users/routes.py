"""Module for users related endpoints."""
from http import HTTPStatus

from flask import Response, jsonify, make_response
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

import src.app.constants.error_messages as errors
from src.app.models.users import Users
from src.app.schemas.user_schemas import UserEdit, UserLogin, UserRegister, UserSchema
from src.app.schemas.wrappers import handle_validation
from src.app.services.user_service import UserService
from src.app.users import bp
from src.app.utils.password_hasher import PasswordHasher


@bp.route("/users/get_current_user", methods=["GET"])
@jwt_required()
def get_current_user() -> Response:
    """Return the user information."""
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user)


@bp.route("/users/login", methods=["POST"])
@handle_validation(schema=UserLogin())
def login(user_data: dict) -> Response:
    """Generate a JWT token for the user."""
    username = user_data["username"]
    password = user_data["password"]

    user = Users.query.filter_by(username=username).first()
    is_password_valid = (
        PasswordHasher.verify_password(password, user.password) if user else False
    )

    if user is None:
        response = {"message": errors.USER_NOT_FOUND}
        return make_response(jsonify(response), HTTPStatus.NOT_FOUND)
    elif not is_password_valid:
        response = {"message": errors.INVALID_PASSWORD}
        return make_response(jsonify(response), HTTPStatus.UNAUTHORIZED)

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)


@bp.route("/users/register", methods=["POST"])
@handle_validation(schema=UserRegister())
def register(user_data: dict) -> Response:
    """Register a new user."""
    username_exists = (
        UserService.get_user_by_username(username=user_data["username"]) is not None
    )

    if username_exists:
        response = {"message": errors.USERNAME_EXISTS}
        return make_response(jsonify(response), HTTPStatus.CONFLICT)

    UserService.create_user(user_data=user_data)

    response = {"message": "User created successfully"}
    return make_response(jsonify(response), HTTPStatus.CREATED)


@bp.route("/users", methods=["GET"])
def get_all_users() -> Response:
    """Return all users."""
    users = UserService.get_all_users()
    user_schema = UserSchema(many=True)
    users_json = user_schema.dump(users)
    return make_response(jsonify(users_json), HTTPStatus.OK)


@bp.route("/users/students", methods=["GET"])
def get_all_students() -> Response:
    """Return all students."""
    students = UserService.get_all_students()
    user_schema = UserSchema(many=True)
    users_json = user_schema.dump(students)
    return make_response(jsonify(users_json), HTTPStatus.OK)


@bp.route("/users/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id: int) -> Response:
    """Return a user by id."""
    user = UserService.get_user_by_id(user_id)
    if user is None:
        response = {"message": "User not found"}
        return make_response(jsonify(response), HTTPStatus.NOT_FOUND)

    user_schema = UserSchema()
    user_json = user_schema.dump(user)
    return make_response(jsonify(user_json), HTTPStatus.OK)


@bp.route("/users/edit_profile", methods=["PUT"])
@jwt_required()
@handle_validation(schema=UserEdit())
def edit_user_profile(edited_user_data: dict) -> Response:
    """Edit the user profile."""
    user_id = get_jwt_identity()

    if user_id is None:
        response = {"message": "Unauthorized - user not logged in"}
        return make_response(jsonify(response), HTTPStatus.UNAUTHORIZED)

    user = UserService.get_user_by_id(user_id=user_id)

    UserService.update_user(
        user=user,
        edited_user_data=edited_user_data,
    )
    response = {"message": "User profile updated successfully"}
    return make_response(jsonify(response), HTTPStatus.OK)
