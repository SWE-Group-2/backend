from src.app.extensions import db


class Roles(db.Model):
    """Model for the Role object."""

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(15), unique=True, nullable=False)

    def __repr__(self) -> str:
        """Return a string representation of the Role."""
        return f"<Role '{self.role}'>"
