"""Module for student related endpoints."""
from src.app.student import bp


@bp.route("/student")
def index() -> str:
    """Return example text for the student blueprint."""
    return "This is the student blueprint."
