"""Module for admin related endpoints."""
from src.app.admin import bp


@bp.route("/admin")
def index() -> str:
    """Return example text for the admin blueprint."""
    return "This is the admin blueprint."
