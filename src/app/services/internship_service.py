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
        company_photo_link: str = None,
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
            company_photo_link=company_photo_link,
        )
        db.session.add(internship)
        db.session.commit()
        return internship

    @staticmethod
    def update_internship_by_id(
        internship_id: int,
        company: str,
        position: str,
        website: str,
        deadline: datetime.date,
        time_period_id: int,
        company_photo_link: str,
    ) -> Internships:
        """Update an internship by its id."""
        internship = Internships.query.filter(Internships.id == internship_id).first()
        internship.company = company
        internship.position = position
        internship.website = website
        internship.deadline = deadline
        internship.time_period_id = time_period_id
        internship.company_photo_link = company_photo_link

        db.session.commit()
        return internship

    @staticmethod
    def get_internships() -> list[Internships]:
        """Return all internships."""
        return Internships.query.all()

    @staticmethod
    def get_internships_by_user(user_id: int) -> list[Internships]:
        """Return all internships by user."""
        return Internships.query.filter(Internships.author_id == user_id).all()

    @staticmethod
    def get_internship(internship_id: int) -> Internships:
        """Return an internship."""
        return Internships.query.filter(Internships.id == internship_id).first()

    @staticmethod
    def delete_internship_by_id(internship_id: int) -> None:
        """Delete an internship by its id."""
        internship = Internships.query.filter(Internships.id == internship_id).first()
        db.session.delete(internship)
        db.session.commit()

    @staticmethod
    def flag_internship(internship_id: int) -> Internships:
        """Flag an internship."""
        internship = Internships.query.filter(Internships.id == internship_id).first()
        internship.flagged = True
        db.session.commit()
        return internship

    @staticmethod
    def unflag_internship(internship_id: int) -> Internships:
        """Unflag an internship."""
        internship = Internships.query.filter(Internships.id == internship_id).first()
        internship.flagged = False
        db.session.commit()
        return internship
