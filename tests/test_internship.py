from datetime import datetime

from flask.testing import FlaskClient

from src.app import db
from src.app.models.internships import Internships


def test_add_internship(test_client: FlaskClient, session: db.session) -> None:
    """Test the add internship endpoint."""
    data = {
        "company": "Wirecard",
        "position": "Facility manager",
        "website": "www.wirecard.com",
        "deadline": "2023-01-01",
        "author_id": 1,
        "time_period_id": 1,
    }
    response = test_client.post("/internships/add_internship", json=data)
    assert response.status_code == 201
    assert response.json == {"message": "Internship created successfully"}
    internship = session.query(Internships).first()
    assert internship.company == "Wirecard"
    assert internship.position == "Facility manager"
    assert internship.website == "www.wirecard.com"
    assert internship.deadline == datetime.strptime("2023-01-01", "%Y-%m-%d").date()
    assert internship.author_id == 1
    assert internship.time_period_id == 1
    assert internship.flagged is False
    assert internship.created_at is not None


def test_add_internship_invalid_request(test_client: FlaskClient) -> None:
    """Test the add internship endpoint with an invalid request."""
    data = {
        "Joe": "Mama",
    }
    response = test_client.post("/internship/add_internship", json=data)
    assert response.status_code == 400
    assert response.json == {"message": "Invalid request body"}


def test_get_internships(test_client: FlaskClient) -> None:
    """Test the get internships endpoint."""
    response = test_client.get("/internships")
    assert response.status_code == 200
    assert response.json == {"internships": []}
