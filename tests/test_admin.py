from flask.testing import FlaskClient

from src.app import db
from src.app.models.roles import RoleEnum
from src.app.models.time_periods import TimePeriods
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


def test_user_deletion_non_admin(
    test_client: FlaskClient, session: db.session, student_access_token: str
) -> None:
    """Test the user deletion endpoint with a non-admin user."""
    response = test_client.delete(
        "/admin/delete_user/1",
        headers={"Authorization": f"Bearer {student_access_token}"},
    )
    assert response.status_code == 401
    assert response.json == {"message": "Unauthorized"}


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


def test_change_role(
    test_client: FlaskClient, session: db.session, admin_access_token: str
) -> None:
    """Test the change role endpoint."""
    user = Users(
        first_name="Test",
        last_name="User",
        username="mynameisjeff",
        password="hardpass",
        role_id=RoleEnum.student.value,
    )
    db.session.add(user)
    db.session.commit()

    data = {
        "role_id": RoleEnum.admin.value,
    }
    response = test_client.put(
        "/admin/change_role/mynameisjeff",
        headers={"Authorization": f"Bearer {admin_access_token}"},
        json=data,
    )
    assert response.status_code == 200
    assert response.json == {"message": "Role changed successfully"}
    user = session.query(Users).filter(Users.username == "mynameisjeff").first()
    assert user.role_id == RoleEnum.admin.value


def test_change_role_invalid_request(
    test_client: FlaskClient, admin_access_token: str
) -> None:
    """Test the change role endpoint with an invalid request."""
    data = {
        "role_id": RoleEnum.admin.value,
    }
    response = test_client.put(
        "/admin/change_role/thisisnotausername1257612401z5",
        headers={"Authorization": f"Bearer {admin_access_token}"},
        json=data,
    )
    assert response.status_code == 404
    assert response.json == {"message": "User not found"}


def test_change_role_non_admin(
    test_client: FlaskClient, session: db.session, student_access_token: str
) -> None:
    """Test the change role endpoint with a non-admin user."""
    user = Users(
        first_name="Test",
        last_name="User",
        username="mynameisjeff",
        password="hardpass",
        role_id=RoleEnum.student.value,
    )
    db.session.add(user)
    db.session.commit()
    data = {
        "role_id": RoleEnum.admin.value,
    }
    response = test_client.put(
        "/admin/change_role/mynameisjeff",
        headers={"Authorization": f"Bearer {student_access_token}"},
        json=data,
    )
    assert response.status_code == 401
    assert response.json == {"message": "Unauthorized"}


def test_delete_time_period(
    test_client: FlaskClient, session: db.session, admin_access_token: str
) -> None:
    """Test the delete time period endpoint."""
    data = {
        "start_date": "2024-08-01",
        "end_date": "2024-08-31",
        "name": "August 2024",
    }
    test_client.post(
        EndpointEnum.add_time_period.value,
        headers={"Authorization": f"Bearer {admin_access_token}"},
        json=data,
    )

    response = test_client.delete(
        "/admin/delete_time_period/1",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == 200
    assert response.json == {"message": "Time period deleted successfully"}
    time_period = session.query(TimePeriods).filter(TimePeriods.id == 1).first()
    assert time_period is None


def test_delete_time_period_invalid_request(
    test_client: FlaskClient, admin_access_token: str
) -> None:
    """Test the delete time period endpoint with an invalid request."""
    response = test_client.delete(
        "/admin/delete_time_period/0",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == 404
    assert response.json == {"message": "Time period not found"}


def test_delete_time_period_non_admin(
    test_client: FlaskClient, session: db.session, student_access_token: str
) -> None:
    """Test the delete time period endpoint with a non-admin user."""
    response = test_client.delete(
        "/admin/delete_time_period/1",
        headers={"Authorization": f"Bearer {student_access_token}"},
    )
    assert response.status_code == 401
    assert response.json == {"message": "Unauthorized"}
