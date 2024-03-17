from src.app.extensions import db


class Flags(db.model):
    """Model for a Flag object."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    internship_id = db.Column(
        db.Integer, db.ForeignKey("internships.id"), nullable=False
    )
    reason = db.Column(db.String(255))

    def __repr__(self) -> str:
        """Return a string representation of the Flag."""
        return f"<Flag '{self.user_id} -> {self.internship_id}'>"
