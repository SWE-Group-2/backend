from src.app.extensions import db


class Internships(db.Model):
    """Model for the Internship object."""

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(255), nullable=False)
    skills_required = db.Column(db.String(255), nullable=False)
    website = db.Column(db.String(255), nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    time_period_id = db.Column(
        db.Integer, db.ForeignKey("time_periods.id"), nullable=False
    )
    flagged = db.Column(db.Boolean, default=False)
    flagged_amount = db.Column(db.Integer, default=0)

    def __repr__(self) -> str:
        """Return a string representation of the Internship."""
        return f"<Internship '{self.company}/{self.position}'>"
