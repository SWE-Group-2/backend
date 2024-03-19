import enum

from src.app.extensions import db


class RoleEnum(enum.Enum):
    """Enum for the role of a User."""

    admin = 1
    instructor = 2
    student = 3

    def __repr__(self) -> str:
        """Return a string representation of the RoleEnum."""
        return f"<RoleEnum '{self.value}'>"


class Roles(db.Model):
    """Model for the Role object."""

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(15), unique=True, nullable=False)

    def __repr__(self) -> str:
        """Return a string representation of the Role."""
        return f"<Role '{self.role}'>"
