from src.app.extensions import db
from src.app.models.roles import RoleEnum
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
    def get_user_by_username(username: str) -> Users:
        """Return a user by username."""
        return Users.query.filter_by(username=username).first()

    @staticmethod
    def get_all_users() -> list[Users]:
        """Return all users."""
        return Users.query.all()

    @staticmethod
    def get_all_students() -> list[Users]:
        """Return all students."""
        return Users.query.filter_by(role_id=RoleEnum.student.value).all()

    @staticmethod
    def get_user_by_id(user_id: int) -> Users:
        """Return a user by id."""
        return Users.query.filter_by(id=user_id).first()
