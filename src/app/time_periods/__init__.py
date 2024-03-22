from flask import Blueprint

bp = Blueprint("time_periods", __name__)

from src.app.time_periods import routes  # noqa: F401, E402
