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
        flagged: bool = False,
        created_at: datetime.datetime = db.func.now(),
    ) -> Internships:
        """Create a new internship."""
        internship = Internships(
            company=company,
            position=position,
            website=website,
            deadline=deadline,
            author_id=author_id,
            time_period_id=time_period_id,
            flagged=flagged,
            created_at=created_at,
        )
        db.session.add(internship)
        db.session.commit()
        return internship

    @staticmethod
    def get_internships() -> list[Internships]:
        """Return all internships."""
        return Internships.query.all()

    @staticmethod
    def get_internship(internship_id: str) -> Internships:
        """Return an internship."""
        return Internships.query.filter(Internships.id == internship_id).first()
