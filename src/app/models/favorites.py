from src.app.extensions import db


class Favorites(db.model):
    """Model for a Favorite object."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    internship_id = db.Column(
        db.Integer, db.ForeignKey("internships.id"), nullable=False
    )

    def __repr__(self) -> str:
        """Return a string representation of the Favorite."""
        return f"<Favorite '{self.user_id} -> {self.internship_id}'>"
