"""Module for users related endpoints."""
from src.app.users import bp


@bp.route("/student")
def index() -> str:
    """Return example text for the users blueprint."""
    return "This is the users blueprint."
