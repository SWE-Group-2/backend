from flask import Blueprint

bp = Blueprint("users", __name__)

from src.app.users import routes  # noqa: F401, E402
