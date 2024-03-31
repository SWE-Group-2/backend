"""Module for internship related endpoints."""
from datetime import datetime

from flask import Response, jsonify, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.app.internship import bp
from src.app.services.flag_service import FlagService
from src.app.services.internship_service import InternshipService
from src.app.services.user_service import UserService


@bp.route("/internships/add_internship", methods=["POST"])
@jwt_required()
def add_internship() -> Response:
    """Create a new internship."""
    try:
        company = request.json["company"]
        position = request.json["position"]
        website = request.json["website"]
        deadline = datetime.strptime(request.json["deadline"], "%Y-%m-%d")
        time_period_id = request.json["time_period_id"]
        company_photo_link = request.json.get("company_photo_link")
    except KeyError:
        response = {"message": "Invalid request body"}
        return make_response(jsonify(response), 400)

    if deadline < datetime.now():
        response = {"message": "Deadline must be in the future"}
        return make_response(jsonify(response), 400)

    InternshipService.create_internship(
        company=company,
        position=position,
        website=website,
        deadline=deadline,
        author_id=get_jwt_identity(),
        time_period_id=time_period_id,
        company_photo_link=company_photo_link,
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
            "id": internship.id,
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


@bp.route("/internships/<int:internship_id>", methods=["GET"])
def view_internship(internship_id: int) -> Response:
    """Return internship information."""
    internship = InternshipService.get_internship(internship_id)

    if internship is None:
        response = {"message": "Internship not found"}
        return make_response(jsonify(response), 404)

    internships_data = {
        "id": internship.id,
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

    return jsonify(internships_data)


@bp.route("/internships/<int:internship_id>", methods=["PUT"])
@jwt_required()
def update_internship(internship_id: int) -> Response:
    """Return example text for the update internship endpoint."""
    internship = InternshipService.get_internship(internship_id)
    user = UserService.get_user_by_id(get_jwt_identity())

    if internship is None:
        response = {"message": "Internship not found"}
        return make_response(jsonify(response), 404)
    elif internship.author_id != user.id and user.role_id != 1:
        response = {"message": "Unauthorized"}
        return make_response(jsonify(response), 401)

    try:
        company = request.json["company"]
        position = request.json["position"]
        website = request.json["website"]
        deadline = datetime.strptime(request.json["deadline"], "%Y-%m-%d")
        time_period_id = request.json["time_period_id"]
        company_photo_link = request.json.get("company_photo_link")
    except KeyError:
        response = {"message": "Invalid request body"}
        return make_response(jsonify(response), 400)

    InternshipService.update_internship_by_id(
        internship_id=internship_id,
        company=company,
        position=position,
        website=website,
        deadline=deadline,
        time_period_id=time_period_id,
        company_photo_link=company_photo_link,
    )

    response = {"message": "Internship updated successfully"}
    return make_response(jsonify(response), 200)


@bp.route("/internships/<int:internship_id>", methods=["DELETE"])
@jwt_required()
def delete_internship(internship_id: int) -> Response:
    """Delete an internship."""
    internship = InternshipService.get_internship(internship_id)
    user = UserService.get_user_by_id(get_jwt_identity())

    if internship is None:
        response = {"message": "Internship not found"}
        return make_response(jsonify(response), 404)
    elif internship.author_id != user.id and user.role_id != 1:
        response = {"message": "Unauthorized"}
        return make_response(jsonify(response), 401)

    InternshipService.delete_internship_by_id(internship_id=internship_id)

    response = {"message": "Internship deleted successfully"}
    return make_response(jsonify(response), 200)


@bp.route("/internships/flag/<int:internship_id>", methods=["PUT"])
@jwt_required()
def flag_internship(internship_id: int) -> Response:
    """Flag an internship."""
    internship = InternshipService.get_internship(internship_id)
    user = UserService.get_user_by_id(get_jwt_identity())

    if internship is None:
        response = {"message": "Internship not found"}
        return make_response(jsonify(response), 404)

    if not FlagService.user_has_flagged(internship_id=internship_id, user_id=user.id):
        FlagService.create_flag(internship_id=internship_id, user_id=user.id)
        InternshipService.flag_internship(internship_id=internship_id)

    response = {"message": "Internship flagged successfully"}
    return make_response(jsonify(response), 200)


@bp.route("/internships/unflag/<int:internship_id>", methods=["PUT"])
@jwt_required()
def unflag_internship(internship_id: int) -> Response:
    """Unflag an internship."""
    internship = InternshipService.get_internship(internship_id)
    user = UserService.get_user_by_id(get_jwt_identity())

    if internship is None:
        response = {"message": "Internship not found"}
        return make_response(jsonify(response), 404)

    if FlagService.user_has_flagged(internship_id=internship_id, user_id=user.id):
        FlagService.delete_flag(internship_id=internship_id, user_id=user.id)

    if FlagService.num_flags(internship_id) == 0:
        InternshipService.unflag_internship(internship_id=internship_id)

    response = {"message": "Internship unflagged successfully"}
    return make_response(jsonify(response), 200)
