"""Package for the app of the application.""" ""
import datetime
import os
from typing import Optional

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_dance.contrib.google import make_google_blueprint
from flask_jwt_extended import JWTManager

from config import Config
from src.app.extensions import db
from src.app.utils.password_hasher import PasswordHasher


def create_app(config: Optional = Config) -> Flask:
    """Create the Flask application."""
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(config)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    CORS(app, resources={r"/*": {"origins": "*"}})
    JWTManager(app)

    google_bp = make_google_blueprint(
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        scope=["email", "profile"],
    )
    app.register_blueprint(google_bp, url_prefix="/login/google")

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

            db.session.commit()

        if not Users.query.filter_by(username="admin").first():
            print("Initializing admin user")
            admin_user = Users(
                username="admin",
                password=PasswordHasher.hash_password(password="hardpass"),
                role_id=1,
            )
            student_user = Users(
                username="student",
                password=PasswordHasher.hash_password(password="hardpass"),
                role_id=3,
            )
            db.session.add(admin_user)
            db.session.add(student_user)
            db.session.commit()

        if TimePeriods.query.count() == 0:
            print("Initializing time periods")
            time_period = TimePeriods(
                name="T3 2023-2024",
                start_date=datetime.datetime.strptime("2024-04-22", "%Y-%m-%d").date(),
                end_date=datetime.datetime.strptime("2024-07-21", "%Y-%m-%d").date(),
            )
            db.session.add(time_period)
            db.session.commit()

        if Internships.query.count() == 0:
            print("Initializing internships")
            internship1 = Internships(
                company="test company",
                position="facility manager",
                website="www.test.com",
                deadline=datetime.datetime.strptime("2021-12-12", "%Y-%m-%d").date(),
                author_id=1,
                time_period_id=1,
                company_photo_link="www.test.com",
                flagged=False,
                created_at=datetime.datetime.strptime("2021-12-12", "%Y-%m-%d").date(),
            )
            internship2 = Internships(
                company="piti company",
                position="head of heads",
                website="www.pititi.com",
                deadline=datetime.datetime.strptime("2021-11-02", "%Y-%m-%d").date(),
                author_id=1,
                time_period_id=1,
                company_photo_link="www.pititi.com",
                flagged=False,
                created_at=datetime.datetime.strptime("2021-12-12", "%Y-%m-%d").date(),
            )
            db.session.add(internship2)
            db.session.add(internship1)

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

    from src.app.time_periods import bp as time_periods_blueprint

    app.register_blueprint(time_periods_blueprint)

    from src.app.upload import bp as upload_blueprint

    app.register_blueprint(upload_blueprint)

    return app
