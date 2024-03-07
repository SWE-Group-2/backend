"""Package for the app of the application.""" ""
from flask import Flask

from config import Config


def create_app() -> Flask:
    """Create the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    from src.app.main import bp as main_blueprint

    app.register_blueprint(main_blueprint)

    from src.app.internship import bp as internship_blueprint

    app.register_blueprint(internship_blueprint)

    from src.app.student import bp as student_blueprint

    app.register_blueprint(student_blueprint)

    from src.app.admin import bp as admin_blueprint

    app.register_blueprint(admin_blueprint)

    return app
