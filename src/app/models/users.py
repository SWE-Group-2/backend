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

    def to_dict(self) -> dict:
        """Return a dictionary representation of the User."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "gpa": self.gpa,
            "academic_year": self.academic_year,
            "github_link": self.github_link,
            "linkedin_link": self.linkedin_link,
            "website_link": self.website_link,
            "profile_picture_link": self.profile_picture_link,
            "email": self.email,
            "phone_number": self.phone_number,
            "description": self.description,
            "role_id": self.role_id,
            "internship_time_period_id": self.internship_time_period_id,
        }
