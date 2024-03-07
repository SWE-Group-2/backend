from flask import Blueprint

bp = Blueprint("student", __name__)

from src.app.student import routes  # noqa: F401, E402
