"""Module for internship related endpoints."""
from datetime import datetime

from flask import Response, jsonify, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.app.internship import bp
from src.app.services.internship_service import InternshipService
from src.app.services.user_service import UserService


@bp.route("/internship")
def index() -> str:
    """Return example text for the internship blueprint."""
    return "This is the internship blueprint."


@bp.route("/internships/add_internship", methods=["POST"])
def add_internship() -> Response:
    """Return example text for the add internship endpoint."""
    try:
        company = request.json["company"]
        position = request.json["position"]
        website = request.json["website"]
        deadline = datetime.strptime(request.json["deadline"], "%Y-%m-%d")
        author_id = request.json["author_id"]
        time_period_id = request.json["time_period_id"]
        company_photo_link = request.json.get("company_photo_link")
    except KeyError:
        response = {"message": "Invalid request body"}
        return make_response(jsonify(response), 400)

    InternshipService.create_internship(
        company,
        position,
        website,
        deadline,
        author_id,
        time_period_id,
        company_photo_link,
    )

    response = {"message": "Internship created successfully"}
    return make_response(jsonify(response), 201)


@bp.route("/internships", methods=["GET"])
def get_internships() -> Response:
    """Return all internships endpoint."""
    internships = InternshipService.get_internships()

    # Convert SQLAlchemy objects to dictionaries for JSON serialization
    internships_data = [
        {
            "company": internship.company,
            "position": internship.position,
            "website": internship.website,
            "deadline": internship.deadline.strftime("%Y-%m-%d"),
            "author_id": internship.author_id,
            "time_period_id": internship.time_period_id,
            "company_photo_link": internship.company_photo_link,
            "flagged": internship.flagged,
            "created_at": internship.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for internship in internships
    ]

    return jsonify(internships_data)


@bp.route("/internships/delete_internship", methods=["DELETE"])
@jwt_required()
def delete_internship() -> Response:
    """Delete internship endpoint."""
    try:
        internship_id = request.json["internship_id"]
    except KeyError:
        response = {"message": "Invalid request body"}
        return make_response(jsonify(response), 400)

    user_id = get_jwt_identity()

    role_id = UserService.get_user_by_id(user_id).role_id

    is_admin = role_id == 1

    internship = InternshipService.get_internship(internship_id)
    if (internship.author_id != user_id) and (is_admin is False):
        response = {"message": "User not authorized to delete this internship"}
        return make_response(jsonify(response), 401)

    InternshipService.delete_internship(internship_id)

    response = {"message": "Internship deleted successfully"}
    return make_response(jsonify(response), 200)
