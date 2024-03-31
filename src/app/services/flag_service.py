"""Service for Flag related logic."""
from src.app.extensions import db
from src.app.models.flags import Flags


class FlagService:
    """Class for Flag related tasks."""

    @staticmethod
    def user_has_flagged(internship_id: int, user_id: int) -> bool:
        """Check if a user has flagged an internship."""
        flag = Flags.query.filter(
            Flags.internship_id == internship_id, Flags.user_id == user_id
        ).first()
        return flag is not None

    @staticmethod
    def create_flag(internship_id: int, user_id: int) -> Flags:
        """Create a new flag."""
        flag = Flags(
            internship_id=internship_id,
            user_id=user_id,
        )
        db.session.add(flag)
        db.session.commit()
        return flag

    @staticmethod
    def delete_flag(internship_id: int, user_id: int) -> None:
        """Delete a flag."""
        flag = Flags.query.filter(
            Flags.internship_id == internship_id, Flags.user_id == user_id
        ).first()
        db.session.delete(flag)
        db.session.commit()

    @staticmethod
    def num_flags(internship_id: int) -> int:
        """Get the number of flags for an internship."""
        flags = Flags.query.filter(Flags.internship_id == internship_id).all()
        return len(flags)
