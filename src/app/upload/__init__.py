from flask import Blueprint

bp = Blueprint("upload", __name__)

from src.app.upload import routes  # noqa: F401, E402
