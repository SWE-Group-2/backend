from src.app import PasswordHasher
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
            password=PasswordHasher.hash_password(password),
            role_id=role_id,
        )
        db.session.add(user)
        db.session.commit()
        return user
