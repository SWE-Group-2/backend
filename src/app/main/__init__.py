from flask import Blueprint

bp = Blueprint("main", __name__)

from src.app.main import routes  # noqa: F401, E402
