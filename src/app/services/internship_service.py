import datetime

from src.app.extensions import db
from src.app.models.internships import Internships


class InternshipService:
    """Service for Internship related tasks."""

    @staticmethod
    def create_internship(
        company: str,
        position: str,
        website: str,
        deadline: datetime.date,
        author_id: int,
        time_period_id: int,
    ) -> Internships:
        """Create a new internship."""
        internship = Internships(
            company=company,
            position=position,
            website=website,
            deadline=deadline,
            author_id=author_id,
            time_period_id=time_period_id,
        )
        db.session.add(internship)
        db.session.commit()
        return internship
