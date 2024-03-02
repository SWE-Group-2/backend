"""Main module of the backend application."""
from flask import Flask

from backend.internship import internship_blueprint

app = Flask(__name__)

app.register_blueprint(internship_blueprint)


@app.route("/")
def hello() -> str:
    """Return a simple "Hello, World!" message in HTML format."""
    return "<h1>Hello, World!</h1>"
