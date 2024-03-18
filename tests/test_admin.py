from datetime import datetime

from flask.testing import FlaskClient

from src.app import db
from src.app.models.time_periods import TimePeriods


def test_add_time_period(test_client: FlaskClient, session: db.session) -> None:
    """Test the add time period endpoint."""
    data = {
        "start_date": "2020-01-01",
        "end_date": "2020-02-01",
        "name": "T1_2020-2021",
    }
    response = test_client.post("/admin/add_time_period", json=data)
    assert response.status_code == 201
    assert response.json == {"message": "Time period added successfully"}
    time_period = session.query(TimePeriods).first()
    assert time_period.start_date == datetime.strptime("2020-01-01", "%Y-%m-%d").date()
    assert time_period.end_date == datetime.strptime("2020-02-01", "%Y-%m-%d").date()
    assert time_period.name == "T1_2020-2021"


def test_add_time_period_invalid_request(test_client: FlaskClient) -> None:
    """Test the add time period endpoint with an invalid request."""
    data = {
        "mr": "bombastic",
    }
    response = test_client.post("/admin/add_time_period", json=data)
    assert response.status_code == 400
    assert response.json == {"message": "Invalid request body"}
