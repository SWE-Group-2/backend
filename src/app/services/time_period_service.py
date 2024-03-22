import datetime

from src.app.extensions import db
from src.app.models.time_periods import TimePeriods


class TimePeriodService:
    """Service for Time Period related tasks."""

    @staticmethod
    def create_time_period(
        start_date: datetime.date, end_date: datetime.date, name: str
    ) -> TimePeriods:
        """Create a new time period."""
        time_period = TimePeriods(start_date=start_date, end_date=end_date, name=name)
        db.session.add(time_period)
        db.session.commit()
        return time_period

    @staticmethod
    def get_time_periods() -> list[TimePeriods]:
        """Return all time periods."""
        return TimePeriods.query.all()

    @staticmethod
    def get_valid_time_periods() -> list[TimePeriods]:
        """Return all valid time periods."""
        return TimePeriods.query.filter(
            TimePeriods.start_date > datetime.date.today()
        ).all()
