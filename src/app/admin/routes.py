"""Module for admin related endpoints."""
import datetime

from flask import Response, jsonify, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.app.admin import bp
from src.app.models.roles import RoleEnum
from src.app.services.time_period_service import TimePeriodService
from src.app.services.user_service import UserService


@bp.route("/admin")
def index() -> str:
    """Return example text for the admin blueprint."""
    return "This is the admin blueprint."


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
