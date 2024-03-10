"""Package for the app of the application.""" ""
from flask import Flask

from config import Config
from src.app.extensions import db


def create_app() -> Flask:
    """Create the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Create the database tables
    from src.app.models.internships import Internships  # noqa: F401
    from src.app.models.roles import Roles  # noqa: F401
    from src.app.models.time_periods import TimePeriods  # noqa: F401
    from src.app.models.users import Users  # noqa: F401

    with app.app_context():
        db.create_all()

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
