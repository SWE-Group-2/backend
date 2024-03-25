from flask.testing import FlaskClient

from src.app import db
from tests.conftest import EndpointEnum


def test_add_time_period(
    test_client: FlaskClient, session: db.session, admin_access_token: str
) -> None:
    """Test the add time period endpoint."""
    data = {
        "start_date": "2024-08-01",
        "end_date": "2024-08-31",
        "name": "August 2024",
    }
    response = test_client.post(
        EndpointEnum.add_time_period.value,
        headers={"Authorization": f"Bearer {admin_access_token}"},
        json=data,
    )
    assert response.status_code == 201
    assert response.json == {
        "message": "Time period added successfully",
    }


def test_add_time_period_invalid_request(
    test_client: FlaskClient, admin_access_token: str
) -> None:
    """Test the add time period endpoint with an invalid request."""
    data = {
        "start_date": "2024-08-01",
    }
    response = test_client.post(
        EndpointEnum.add_time_period.value,
        headers={"Authorization": f"Bearer {admin_access_token}"},
        json=data,
    )
    assert response.status_code == 400
    assert response.json == {
        "message": "Invalid request body",
    }


def test_add_time_period_non_admin(
    test_client: FlaskClient, session: db.session, student_access_token: str
) -> None:
    """Test the add time period endpoint with a non-admin user."""
    data = {
        "start_date": "2024-08-01",
        "end_date": "2024-08-31",
        "name": "August 2024",
    }
    response = test_client.post(
        EndpointEnum.add_time_period.value,
        headers={"Authorization": f"Bearer {student_access_token}"},
        json=data,
    )
    assert response.status_code == 401
    assert response.json == {
        "message": "Unauthorized",
    }
