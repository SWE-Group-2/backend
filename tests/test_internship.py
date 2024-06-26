from datetime import datetime

from flask.testing import FlaskClient

from src.app import db
from src.app.models.flags import Flags
from src.app.models.internships import Internships
from tests.conftest import EndpointEnum


def get_token(test_client: FlaskClient) -> str:
    """Get the token for the admin user."""
    response = test_client.post(
        EndpointEnum.login.value, json={"username": "admin", "password": "hardpass"}
    )
    return response.json["access_token"]


def test_add_internship(
    test_client: FlaskClient, session: db.session, admin_access_token: str
) -> None:
    """Test the add internship endpoint."""
    data = {
        "company": "Test Company",
        "position": "Facility manager",
        "website": "www.wirecard.com",
        "deadline": "2069-01-01",
        "author_id": 1,
        "time_period_id": 1,
    }
    response = test_client.post(
        "/internships/add_internship",
        json=data,
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == 201
    assert response.json == {"message": "Internship created successfully"}
    internship = (
        session.query(Internships).filter(Internships.company == "Test Company").first()
    )
    assert internship.company == "Test Company"
    assert internship.position == "Facility manager"
    assert internship.website == "www.wirecard.com"
    assert internship.deadline == datetime.strptime("2069-01-01", "%Y-%m-%d").date()
    assert internship.author_id == 1
    assert internship.time_period_id == 1
    assert internship.flagged is False
    assert internship.created_at is not None


def test_add_internship_invalid_deadline(
    test_client: FlaskClient, admin_access_token: str
) -> None:
    """Test the add internship endpoint with an invalid deadline."""
    data = {
        "company": "Test Company",
        "position": "Facility manager",
        "website": "www.wirecard.com",
        "deadline": "2020-01-01",
        "author_id": 1,
        "time_period_id": 1,
    }
    response = test_client.post(
        "/internships/add_internship",
        json=data,
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == 400
    assert response.json == {"message": "Deadline must be in the future"}


def test_add_internship_invalid_request(
    test_client: FlaskClient, admin_access_token: str
) -> None:
    """Test the add internship endpoint with an invalid request."""
    data = {
        "Joe": "Mama",
    }
    response = test_client.post(
        "/internships/add_internship",
        json=data,
        headers={"Authorization": f"Bearer {admin_access_token}"},
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
    test_client: FlaskClient, session: db.session, admin_access_token: str
) -> None:
    """Test the view internship endpoint with invalid internship id."""
    response = test_client.get(
        "/internships/1", headers={"Authorization": f"Bearer {admin_access_token}"}
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
    test_client: FlaskClient, session: db.session, admin_access_token: str
) -> None:
    """Test the view internship endpoint."""
    response = test_client.get(
        "/internships/0", headers={"Authorization": f"Bearer {admin_access_token}"}
    )

    assert response.status_code == 404
    assert response.json == {"message": "Internship not found"}


def test_update_internship(test_client: FlaskClient, session: db.session) -> None:
    """Test the update internship endpoint."""
    data = {
        "company": "Baller company",
        "position": "Baller",
        "website": "www.baller.com",
        "deadline": "2025-01-01",
        "time_period_id": 1,
        "company_photo_link": "www.baller.com/photo.jpg",
    }
    response = test_client.put(
        "/internships/1",
        json=data,
        headers={"Authorization": f"Bearer {get_token(test_client)}"},
    )
    assert response.status_code == 200
    assert response.json == {"message": "Internship updated successfully"}
    internship = session.query(Internships).filter(Internships.id == 1).first()
    assert internship.company == "Baller company"
    assert internship.position == "Baller"
    assert internship.website == "www.baller.com"
    assert internship.deadline == datetime.strptime("2025-01-01", "%Y-%m-%d").date()
    assert internship.time_period_id == 1


def test_admin_update_internship(
    test_client: FlaskClient, session: db.session, admin_access_token: str
) -> None:
    """Test the update internship endpoint with an admin user."""
    new_internship = Internships(
        company="User 2's company",
        position="facility manager",
        website="www.test.com",
        deadline=datetime.strptime("2021-12-12", "%Y-%m-%d").date(),
        author_id=2,
        time_period_id=1,
        company_photo_link="www.test.com",
        flagged=False,
        created_at=datetime.strptime("2021-12-12", "%Y-%m-%d").date(),
    )
    session.add(new_internship)
    session.commit()

    data = {
        "company": "USER 2'S BALLER COMPANY",
        "position": "Baller",
        "website": "www.baller.com",
        "deadline": "2025-01-01",
        "time_period_id": 1,
        "company_photo_link": "www.baller.com/photo.jpg",
    }

    response = test_client.put(
        f"/internships/{new_internship.id}",
        json=data,
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )

    assert response.status_code == 200
    assert response.json == {"message": "Internship updated successfully"}


def test_non_admin_update_other_user_internship(
    test_client: FlaskClient, session: db.session, student_access_token: str
) -> None:
    """Test the update internship endpoint with an unauthorized user."""
    data = {
        "company": "USER 2'S BALLER COMPANY",
        "position": "Baller",
        "website": "www.baller.com",
        "deadline": "2025-01-01",
        "time_period_id": 1,
        "company_photo_link": "www.baller.com/photo.jpg",
    }

    response = test_client.put(
        "/internships/1",
        json=data,
        headers={"Authorization": f"Bearer {student_access_token}"},
    )
    assert response.status_code == 401
    assert response.json == {"message": "Unauthorized"}


def test_update_internship_invalid_request(test_client: FlaskClient) -> None:
    data = {
        "company_name": "Baller company",
    }
    response = test_client.put(
        "/internships/1",
        json=data,
        headers={"Authorization": f"Bearer {get_token(test_client)}"},
    )

    assert response.status_code == 400
    assert response.json == {"message": "Invalid request body"}


def test_delete_internship(test_client: FlaskClient, session: db.session) -> None:
    """Test the delete internship endpoint."""
    response = test_client.delete(
        "/internships/1", headers={"Authorization": f"Bearer {get_token(test_client)}"}
    )
    assert response.status_code == 200
    assert response.json == {"message": "Internship deleted successfully"}
    internship = session.query(Internships).filter(Internships.id == 1).first()
    assert internship is None


def test_delete_internship_dne(test_client: FlaskClient, session: db.session) -> None:
    """Test the delete internship endpoint."""
    response = test_client.delete(
        "/internships/0", headers={"Authorization": f"Bearer {get_token(test_client)}"}
    )
    assert response.status_code == 404
    assert response.json == {"message": "Internship not found"}


def test_admin_delete_internship(
    test_client: FlaskClient, session: db.session, admin_access_token: str
) -> None:
    """Test the delete internship endpoint with admin."""
    new_internship = Internships(
        company="User 2's company",
        position="facility manager",
        website="www.test.com",
        deadline=datetime.strptime("2021-12-12", "%Y-%m-%d").date(),
        author_id=2,
        time_period_id=1,
        company_photo_link="www.test.com",
        flagged=False,
        created_at=datetime.strptime("2021-12-12", "%Y-%m-%d").date(),
    )
    session.add(new_internship)
    session.commit()

    response = test_client.delete(
        f"/internships/{new_internship.id}",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == 200
    assert response.json == {"message": "Internship deleted successfully"}


def test_non_admin_delete_other_user_internship(
    test_client: FlaskClient, session: db.session, student_access_token: str
) -> None:
    """Test the delete internship endpoint with an unauthorized user."""
    response = test_client.delete(
        "/internships/1",
        headers={"Authorization": f"Bearer {student_access_token}"},
    )
    assert response.status_code == 401
    assert response.json == {"message": "Unauthorized"}


def test_flag_internship(test_client: FlaskClient, session: db.session) -> None:
    """Test the flag internship endpoint."""
    response = test_client.put(
        EndpointEnum.flag_internship.value.format(internship_id=1),
        headers={"Authorization": f"Bearer {get_token(test_client)}"},
    )
    assert response.status_code == 200
    assert response.json == {"message": "Internship flagged successfully"}
    internship = session.query(Internships).filter(Internships.id == 1).first()
    assert internship.flagged is True
    flag = session.query(Flags).filter(Flags.internship_id == 1).first()
    assert flag.internship_id == 1
    assert flag.user_id == 1


def test_flag_internship_dne(test_client: FlaskClient) -> None:
    """Test the flag internship endpoint with invalid internship id."""
    response = test_client.put(
        EndpointEnum.flag_internship.value.format(internship_id=0),
        headers={"Authorization": f"Bearer {get_token(test_client)}"},
    )
    assert response.status_code == 404
    assert response.json == {"message": "Internship not found"}


def test_unflag_internship(test_client: FlaskClient, session: db.session) -> None:
    """Test the unflag internship endpoint."""
    flag = Flags(internship_id=1, user_id=1)
    session.add(flag)
    session.commit()

    internship = session.query(Internships).filter(Internships.id == 1).first()
    internship.flagged = True
    session.commit()

    response = test_client.put(
        EndpointEnum.unflag_internship.value.format(internship_id=1),
        headers={"Authorization": f"Bearer {get_token(test_client)}"},
    )
    assert response.status_code == 200
    assert response.json == {"message": "Internship unflagged successfully"}
    internship = session.query(Internships).filter(Internships.id == 1).first()
    assert internship.flagged is False

    flag = session.query(Flags).filter(Flags.internship_id == 1).first()
    assert flag is None


def test_unflag_internship_dne(test_client: FlaskClient) -> None:
    """Test the unflag internship endpoint with invalid internship id."""
    response = test_client.put(
        EndpointEnum.unflag_internship.value.format(internship_id=0),
        headers={"Authorization": f"Bearer {get_token(test_client)}"},
    )
    assert response.status_code == 404
    assert response.json == {"message": "Internship not found"}
