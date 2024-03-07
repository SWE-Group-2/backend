from src.app.main import bp


@bp.route("/")
def index() -> str:
    """Return example text for the main blueprint."""
    return "This is the main blueprint."
