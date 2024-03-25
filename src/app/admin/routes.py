"""Module for admin related endpoints."""
from flask import Response, jsonify, make_response
from flask_jwt_extended import jwt_required

from src.app.admin import bp
from src.app.services.admin_service import AdminService
from src.app.services.user_service import UserService


@bp.route("/admin")
def index() -> str:
    """Return example text for the admin blueprint."""
    return "This is the admin blueprint."


@bp.route("/admin/delete_user/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id: int) -> Response:
    """Delete a user by id."""
    user = UserService.get_user_by_id(user_id)
    if user is None:
        response = {"message": "User not found"}
        return make_response(jsonify(response), 404)

    AdminService.delete_user_by_id(user_id)
    response = {"message": "User deleted successfully"}
    return make_response(jsonify(response), 200)
