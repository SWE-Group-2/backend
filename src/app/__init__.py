"""Package for the app of the application.""" ""
from typing import Optional

from flask import Flask
from flask_cors import CORS

from config import Config
from src.app.extensions import db
from src.app.utils.password_hasher import PasswordHasher


def create_app(config: Optional = Config) -> Flask:
    """Create the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

    # Initialize extensions
    db.init_app(app)

    # Create the database tables
    from src.app.models.internships import Internships  # noqa: F401
    from src.app.models.roles import Roles  # noqa: F401
    from src.app.models.time_periods import TimePeriods  # noqa: F401
    from src.app.models.users import Users  # noqa: F401

    with app.app_context():
        print("Creating DB")
        db.create_all()

        if Roles.query.count() == 0:
            print("Initializing roles")
            admin_role = Roles(role="Admin")
            instructor_role = Roles(role="Instructor")
            student_role = Roles(role="Student")
            db.session.add(admin_role)
            db.session.add(instructor_role)
            db.session.add(student_role)

        if not Users.query.filter_by(username="admin").first():
            print("Initializing admin user")
            admin_user = Users(
                username="admin",
                password=PasswordHasher.hash_password(password="hardpass"),
                role_id=1,
            )
            db.session.add(admin_user)

        db.session.commit()

    # Register blueprints
    from src.app.main import bp as main_blueprint

    app.register_blueprint(main_blueprint)

    from src.app.internship import bp as internship_blueprint

    app.register_blueprint(internship_blueprint)

    from src.app.users import bp as users_blueprint

    app.register_blueprint(users_blueprint)

    from src.app.admin import bp as admin_blueprint

    app.register_blueprint(admin_blueprint)

    return app
