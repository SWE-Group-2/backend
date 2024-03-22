from datetime import datetime

from flask.testing import FlaskClient

from src.app import db
from src.app.models.internships import Internships


def test_add_internship(
    test_client: FlaskClient, session: db.session, access_token: str
) -> None:
    """Test the add internship endpoint."""
    data = {
        "company": "Test Company",
        "position": "Facility manager",
        "website": "www.wirecard.com",
        "deadline": "2023-01-01",
        "author_id": 1,
        "time_period_id": 1,
    }
    response = test_client.post(
        "/internships/add_internship",
        json=data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    assert response.json == {"message": "Internship created successfully"}
    internship = (
        session.query(Internships).filter(Internships.company == "Test Company").first()
    )
    assert internship.company == "Test Company"
    assert internship.position == "Facility manager"
    assert internship.website == "www.wirecard.com"
    assert internship.deadline == datetime.strptime("2023-01-01", "%Y-%m-%d").date()
    assert internship.author_id == 1
    assert internship.time_period_id == 1
    assert internship.flagged is False
    assert internship.created_at is not None


def test_add_internship_invalid_request(
    test_client: FlaskClient, access_token: str
) -> None:
    """Test the add internship endpoint with an invalid request."""
    data = {
        "Joe": "Mama",
    }
    response = test_client.post(
        "/internships/add_internship",
        json=data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 400
    assert response.json == {"message": "Invalid request body"}


def test_get_internships(test_client: FlaskClient, session: db.session) -> None:
    """Test the get internships endpoint."""
    response = test_client.get("/internships")
    internship = session.query(Internships).first()
    internship_json = {
        "id": internship.id,
        "company": internship.company,
        "position": internship.position,
        "website": internship.website,
        "deadline": internship.deadline.strftime("%Y-%m-%d"),
        "author_id": internship.author_id,
        "time_period_id": internship.time_period_id,
        "company_photo_link": internship.company_photo_link,
        "flagged": internship.flagged,
        "created_at": internship.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    }
    assert response.status_code == 200
    assert response.json[0] == internship_json


def test_view_internship(
    test_client: FlaskClient, session: db.session, access_token: str
) -> None:
    """Test the view internship endpoint with invalid internship id."""
    response = test_client.get(
        "/internships/1", headers={"Authorization": f"Bearer {access_token}"}
    )
    internship = session.query(Internships).filter(Internships.id == 1).first()

    assert response.status_code == 200
    assert response.json["id"] == 1
    assert response.json["company"] == internship.company
    assert response.json["position"] == internship.position
    assert response.json["website"] == internship.website
    assert response.json["deadline"] == internship.deadline.strftime("%Y-%m-%d")
    assert response.json["author_id"] == internship.author_id
    assert response.json["time_period_id"] == internship.time_period_id
    assert response.json["company_photo_link"] == internship.company_photo_link
    assert response.json["flagged"] == internship.flagged
    assert response.json["created_at"] == internship.created_at.strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def test_view_internship_dne(
    test_client: FlaskClient, session: db.session, access_token: str
) -> None:
    """Test the view internship endpoint."""
    response = test_client.get(
        "/internships/0", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 404
    assert response.json == {"message": "Internship not found"}
