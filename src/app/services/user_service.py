from src.app.extensions import db
from src.app.models.users import Users


class UserService:
    """Service for User related tasks."""

    @staticmethod
    def create_user(
        first_name: str,
        last_name: str,
        username: str,
        password: str,
        role_id: int,
    ) -> Users:
        """Create a new user."""
        user = Users(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            role_id=role_id,
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update_user(
        user: Users,
        first_name: str,
        last_name: str,
        gpa: float,
        academic_year: str,
        github_link: str,
        linkedin_link: str,
        website_link: str,
        profile_picture_link: str,
        email: str,
        phone_number: str,
        description: str,
        role_id: int,
        internship_time_period_id: int,
    ) -> Users:
        """Update a user."""
        user.first_name = first_name
        user.last_name = last_name
        user.gpa = gpa
        user.academic_year = academic_year
        user.github_link = github_link
        user.linkedin_link = linkedin_link
        user.website_link = website_link
        user.profile_picture_link = profile_picture_link
        user.email = email
        user.phone_number = phone_number
        user.description = description
        user.role_id = role_id
        user.internship_time_period_id = internship_time_period_id
        db.session.commit()
        return user

    @staticmethod
    def get_user_by_username(username: str) -> Users:
        """Return a user by username."""
        return Users.query.filter_by(username=username).first()

    @staticmethod
    def get_user_by_id(user_id: int) -> Users:
        """Return a user by id."""
        return Users.query.filter_by(id=user_id).first()
