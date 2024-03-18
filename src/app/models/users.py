from src.app.extensions import db


class Users(db.Model):
    """Model for a User of the site."""

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False)
    gpa = db.Column(db.Float)
    academic_year = db.Column(db.String(255))
    github_link = db.Column(db.String(255))
    linkedin_link = db.Column(db.String(255))
    website_link = db.Column(db.String(255))
    profile_picture_link = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    description = db.Column(db.String(500))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    internship_time_period_id = db.Column(db.Integer, db.ForeignKey("time_periods.id"))

    def __repr__(self) -> str:
        """Return a string representation of the User."""
        return f"<User '{self.username}'>"
