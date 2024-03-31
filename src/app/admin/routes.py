"""Module for admin related endpoints."""
import datetime

from flask import Response, jsonify, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.orm.exc import UnmappedInstanceError

from src.app.admin import bp
from src.app.models.roles import RoleEnum
from src.app.services.admin_service import AdminService
from src.app.services.flag_service import FlagService
from src.app.services.internship_service import InternshipService
from src.app.services.time_period_service import TimePeriodService
from src.app.services.user_service import UserService


@bp.route("/admin")
def index() -> str:
    """Return example text for the admin blueprint."""
    return "This is the admin blueprint."


@bp.route("/admin/delete_user/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id: int) -> Response:
    """Delete a user by id."""
    current_user = UserService.get_user_by_id(get_jwt_identity())
    user = UserService.get_user_by_id(user_id)
    if user is None:
        response = {"message": "User not found"}
        return make_response(jsonify(response), 404)
    elif current_user.role_id != RoleEnum.admin.value:
        response = {"message": "Unauthorized"}
        return make_response(jsonify(response), 401)

    AdminService.delete_user_by_id(user_id)
    response = {"message": "User deleted successfully"}
    return make_response(jsonify(response), 200)


@bp.route("/admin/add_time_period", methods=["POST"])
@jwt_required()
def add_time_period() -> Response:
    """Add a new time period."""
    user = UserService.get_user_by_id(get_jwt_identity())

    if user.role_id != RoleEnum.admin.value:
        response = {"message": "Unauthorized"}
        return make_response(jsonify(response), 401)

    try:
        start_date = datetime.datetime.strptime(
            request.json["start_date"], "%Y-%m-%d"
        ).date()
        end_date = datetime.datetime.strptime(
            request.json["end_date"], "%Y-%m-%d"
        ).date()
        name = request.json["name"]
    except KeyError:
        response = {"message": "Invalid request body"}
        return make_response(jsonify(response), 400)

    TimePeriodService.add_time_period(start_date, end_date, name)
    response = {"message": "Time period added successfully"}
    return make_response(jsonify(response), 201)


@bp.route("/admin/change_role/<string:username>", methods=["PUT"])
@jwt_required()
def change_role(username: str) -> Response:
    """Change the role of a user."""
    current_user = UserService.get_user_by_id(get_jwt_identity())
    user = UserService.get_user_by_username(username)
    if user is None:
        response = {"message": "User not found"}
        return make_response(jsonify(response), 404)
    elif current_user.role_id != RoleEnum.admin.value:
        response = {"message": "Unauthorized"}
        return make_response(jsonify(response), 401)

    try:
        role_id = request.json["role_id"]
    except KeyError:
        response = {"message": "Invalid request body"}
        return make_response(jsonify(response), 400)

    AdminService.change_user_role_by_username(username, role_id)
    response = {"message": "Role changed successfully"}
    return make_response(jsonify(response), 200)


@bp.route("/admin/delete_time_period/<int:time_period_id>", methods=["DELETE"])
@jwt_required()
def delete_time_period(time_period_id: int) -> Response:
    """Delete a time period."""
    current_user = UserService.get_user_by_id(get_jwt_identity())

    if current_user.role_id != RoleEnum.admin.value:
        response = {"message": "Unauthorized"}
        return make_response(jsonify(response), 401)
    try:
        TimePeriodService.delete_time_period_by_id(time_period_id)
    except UnmappedInstanceError:
        response = {"message": "Time period not found"}
        return make_response(jsonify(response), 404)
    response = {"message": "Time period deleted successfully"}
    return make_response(jsonify(response), 200)


@bp.route("/internships/clear_flags/<int:internship_id>", methods=["PUT"])
@jwt_required()
def clear_flags(internship_id: int) -> Response:
    """Clear all flags for an internship."""
    internship = InternshipService.get_internship(internship_id)
    user = UserService.get_user_by_id(get_jwt_identity())

    if internship is None:
        response = {"message": "Internship not found"}
        return make_response(jsonify(response), 404)
    elif user.role_id != RoleEnum.admin.value:
        response = {"message": "Unauthorized"}
        return make_response(jsonify(response), 401)

    FlagService.clear_flags(internship_id=internship_id)
    InternshipService.unflag_internship(internship_id=internship_id)

    response = {"message": "Flags cleared successfully"}
    return make_response(jsonify(response), 200)
