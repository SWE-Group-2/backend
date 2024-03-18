from src.app.extensions import db


class Internships(db.Model):
    """Model for the Internship object."""

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(255), nullable=False)
    website = db.Column(db.String(255), nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    time_period_id = db.Column(
        db.Integer, db.ForeignKey("time_periods.id"), nullable=False
    )
    company_photo_link = db.Column(db.String(255))
    flagged = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self) -> str:
        """Return a string representation of the Internship."""
        return f"<Internship '{self.company}/{self.position}'>"
