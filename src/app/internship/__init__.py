from flask import Blueprint

bp = Blueprint("internship", __name__)

from src.app.internship import routes  # noqa: F401, E402
