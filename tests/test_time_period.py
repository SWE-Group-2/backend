from flask.testing import FlaskClient

from src.app.extensions import db


def test_get_all_time_periods(test_client: FlaskClient, session: db.session) -> None:
    """Test the get all time periods endpoint."""
    response = test_client.get("/time_periods")
    time_period_json = {
        "id": 1,
        "start_date": "2024-04-22",
        "end_date": "2024-07-21",
        "name": "T3 2023-2024",
    }

    assert response.status_code == 200
    assert response.json[0] == time_period_json
