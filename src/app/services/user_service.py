from src.app.extensions import db
from src.app.models.roles import RoleEnum
from src.app.models.users import Users
from src.app.utils.password_hasher import PasswordHasher


class UserService:
    """Service for User related tasks."""

    @staticmethod
    def create_user(user_data: dict) -> Users:
        """Create a new user."""
        user = Users(
            username=user_data["username"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            password=PasswordHasher.hash_password(user_data["password"]),
            role_id=RoleEnum.student.value,
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update_user(
        user: Users,
        edited_user_data: dict,
    ) -> Users:
        """Update a user."""
        for key, value in edited_user_data.items():
            setattr(user, key, value)
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
