from flask import Blueprint

bp = Blueprint("admin", __name__)

from src.app.admin import routes  # noqa: F401, E402
