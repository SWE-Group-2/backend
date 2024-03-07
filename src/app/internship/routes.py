"""Module for internship related endpoints."""
from src.app.internship import bp


@bp.route("/internship")
def index() -> str:
    """Return example text for the internship blueprint."""
    return "This is the internship blueprint."
