"""Module for admin related endpoints."""
from datetime import datetime

from flask import Response, jsonify, make_response, request

from src.app.admin import bp
from src.app.services.admin_service import AdminService


@bp.route("/admin")
def index() -> str:
    """Return example text for the admin blueprint."""
    return "This is the admin blueprint."


@bp.route("/admin/add_time_period", methods=["POST"])
def add_time_period() -> Response:
    """Return example text for the add time period endpoint."""
    start_date = datetime.strptime(request.json["start_date"], "%Y-%m-%d")
    end_date = datetime.strptime(request.json["end_date"], "%Y-%m-%d")
    name = request.json["name"]

    AdminService.create_time_period(start_date, end_date, name)

    response = {"message": "Time period added successfully"}
    return make_response(jsonify(response), 201)
