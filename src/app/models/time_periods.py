from src.app.extensions import db


class TimePeriods(db.Model):
    """Model for a specific trimester's time period (e.g., T2 2023_2024)."""

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self) -> str:
        """Return a string representation of the TimePeriod."""
        return f"<TimePeriod '{self.name}'>"
