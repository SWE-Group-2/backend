"""Module for users related endpoints."""
from flask import Response, jsonify, make_response, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from src.app.models.roles import RoleEnum
from src.app.models.users import Users
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


@bp.route("/users", methods=["GET"])
def get_all_users() -> Response:
    """Return all users."""
    users = UserService.get_all_users()
    users_json = [
        {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "gpa": user.gpa,
            "academic_year": user.academic_year,
            "github_link": user.github_link,
            "linkedin_link": user.linkedin_link,
            "website_link": user.website_link,
            "profile_picture_link": user.profile_picture_link,
            "email": user.email,
            "phone_number": user.phone_number,
            "description": user.description,
            "role_id": user.role_id,
            "internship_time_period_id": user.internship_time_period_id,
        }
        for user in users
    ]

    return jsonify(users_json)


@bp.route("/users/students", methods=["GET"])
def get_all_students() -> Response:
    """Return all students."""
    students = UserService.get_all_students()
    students_json = [
        {
            "id": student.id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "username": student.username,
            "gpa": student.gpa,
            "academic_year": student.academic_year,
            "github_link": student.github_link,
            "linkedin_link": student.linkedin_link,
            "website_link": student.website_link,
            "profile_picture_link": student.profile_picture_link,
            "email": student.email,
            "phone_number": student.phone_number,
            "description": student.description,
            "role_id": student.role_id,
            "internship_time_period_id": student.internship_time_period_id,
        }
        for student in students
    ]

    return jsonify(students_json)


@bp.route("/users/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id: int) -> Response:
    """Return a user by id."""
    user = UserService.get_user_by_id(user_id)
    if user is None:
        response = {"message": "User not found"}
        return make_response(jsonify(response), 404)

    user_json = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "gpa": user.gpa,
        "academic_year": user.academic_year,
        "github_link": user.github_link,
        "linkedin_link": user.linkedin_link,
        "website_link": user.website_link,
        "profile_picture_link": user.profile_picture_link,
        "email": user.email,
        "phone_number": user.phone_number,
        "description": user.description,
        "role_id": user.role_id,
        "internship_time_period_id": user.internship_time_period_id,
    }

    return jsonify(user_json)


@bp.route("/users/edit_profile", methods=["PUT"])
@jwt_required()
def edit_user_profile() -> Response:
    """Edit the user profile."""
    user_id = get_jwt_identity()

    # Should never be true because of jwt.
    if user_id is None:
        response = {"message": "Unauthorized - user not logged in"}
        return make_response(jsonify(response), 401)

    user = UserService.get_user_by_id(user_id=user_id)

    try:
        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        gpa = request.json["gpa"]
        academic_year = request.json["academic_year"]
        github_link = request.json["github_link"]
        linkedin_link = request.json["linkedin_link"]
        website_link = request.json["website_link"]
        profile_picture_link = request.json["profile_picture_link"]
        email = request.json["email"]
        phone_number = request.json["phone_number"]
        description = request.json["description"]
        internship_time_period_id = request.json[
            "internship_time_period_id"
        ]  # need to deal with this somewhere
    except KeyError:
        response = {"message": "Invalid request body"}
        return make_response(jsonify(response), 400)

    role_id = user.role_id

    UserService.update_user(
        user=user,
        first_name=first_name,
        last_name=last_name,
        gpa=gpa,
        academic_year=academic_year,
        github_link=github_link,
        linkedin_link=linkedin_link,
        website_link=website_link,
        profile_picture_link=profile_picture_link,
        email=email,
        phone_number=phone_number,
        description=description,
        role_id=role_id,
        internship_time_period_id=internship_time_period_id,
    )
    response = {"message": "User profile updated successfully"}
    return make_response(jsonify(response), 200)
