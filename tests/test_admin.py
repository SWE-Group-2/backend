from flask.testing import FlaskClient

from src.app import db
from src.app.models.roles import RoleEnum
from src.app.models.users import Users
from tests.conftest import EndpointEnum


def test_user_deletion(
    test_client: FlaskClient, session: db.session, admin_access_token: str
) -> None:
    """Test the user deletion endpoint."""
    user = Users(
        first_name="Test",
        last_name="User",
        username="testuser",
        password="hardpass",
        role_id=RoleEnum.student.value,
    )
    db.session.add(user)
    db.session.commit()

    response = test_client.delete(
        f"/admin/delete_user/{user.id}",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == 200
    assert response.json == {"message": "User deleted successfully"}
    user = session.query(Users).filter(Users.username == "testuser").first()
    assert user is None


def test_user_deletion_invalid_request(
    test_client: FlaskClient, admin_access_token: str
) -> None:
    """Test the user deletion endpoint with an invalid request."""
    response = test_client.delete(
        "/admin/delete_user/0",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == 404
    assert response.json == {"message": "User not found"}


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
