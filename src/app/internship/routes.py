"""Module for internship related endpoints."""
from datetime import datetime

from flask import Response, jsonify, make_response, request

from src.app.internship import bp
from src.app.services.internship_service import InternshipService


@bp.route("/internship")
def index() -> str:
    """Return example text for the internship blueprint."""
    return "This is the internship blueprint."


@bp.route("/internship/add_internship", methods=["POST"])
def add_internship() -> Response:
    """Return example text for the add internship endpoint."""
    try:
        company = request.json["company"]
        position = request.json["position"]
        website = request.json["website"]
        deadline = datetime.strptime(request.json["deadline"], "%Y-%m-%d")
        author_id = request.json["author_id"]
        time_period_id = request.json["time_period_id"]
    except KeyError:
        response = {"message": "Invalid request body"}
        return make_response(jsonify(response), 400)

    InternshipService.create_internship(
        company, position, website, deadline, author_id, time_period_id
    )

    response = {"message": "Time period added successfully"}
    return make_response(jsonify(response), 201)
