from src.app.extensions import db
from src.app.models.users import Users


class AdminService:
    """Service for Admin related tasks."""

    @staticmethod
    def delete_user_by_id(user_id: int) -> None:
        """Delete a user by id."""
        user = Users.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()

    @staticmethod
    def change_user_role_by_id(user_id: int, role_id: int) -> None:
        """Change a user's role by id."""
        user = Users.query.filter_by(id=user_id).first()
        user.role_id = role_id
        db.session.commit()
