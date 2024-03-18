from datetime import datetime

from flask.testing import FlaskClient

from src.app import db
from src.app.models.internships import Internships


def test_create_internship(test_client: FlaskClient, session: db.session) -> None:
    """Test the create internship endpoint."""
    data = {
        "company": "The Gang Technology",
        "position": "Backend Engineer",
        "website": "https://thegang.tech/career/v/backend-engineer/",
        "deadline": "2023-04-30",
        "author_id": 1,
        "time_period_id": 1,
    }
    response = test_client.post("/internships/create_internship", json=data)
    assert response.status_code == 201
    assert response.json == {"message": "Internship created successfully"}
    internship = session.query(Internships).first()
    assert internship.company == "The Gang Technology"
    assert internship.position == "Backend Engineer"
    assert internship.website == "https://thegang.tech/career/v/backend-engineer/"
    assert internship.deadline == datetime.strptime("2023-04-30", "%Y-%m-%d").date()
    assert internship.author_id == 1
    assert internship.time_period_id == 1


def test_create_internship_invalid_request(test_client: FlaskClient) -> None:
    """Test the create internship endpoint with an invalid request."""
    data = {
        "mr": "bombastic",
    }
    response = test_client.post("/internships/create_internship", json=data)
    assert response.status_code == 400
    assert response.json == {"message": "Invalid request body"}
