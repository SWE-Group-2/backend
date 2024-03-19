from flask.testing import FlaskClient

from src.app import db
from src.app.models.roles import RoleEnum
from src.app.models.users import Users
from tests.conftest import EndpointEnum


def test_login(test_client: FlaskClient, session: db.session) -> None:
    """Test the login endpoint."""
    data = {"username": "admin", "password": "hardpass"}
    response = test_client.post(EndpointEnum.login.value, json=data)
    assert response.status_code == 200
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = test_client.get(
        EndpointEnum.get_current_user.value,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert response.json == {"logged_in_as": 1}


def test_login_invalid_request(test_client: FlaskClient) -> None:
    """Test the login endpoint with an invalid request."""
    data = {
        "obama": "prism",
    }
    response = test_client.post(EndpointEnum.login.value, json=data)
    assert response.status_code == 400
    assert response.json == {"message": "Invalid request"}


def test_login_user_not_found(test_client: FlaskClient) -> None:
    """Test the login endpoint with a user not found."""
    data = {
        "username": "obama",
        "password": "prism",
    }
    response = test_client.post(EndpointEnum.login.value, json=data)
    assert response.status_code == 404
    assert response.json == {"message": "User not found"}


def test_login_invalid_password(test_client: FlaskClient) -> None:
    """Test the login endpoint with an invalid password."""
    data = {
        "username": "admin",
        "password": "wrongpass",
    }
    response = test_client.post(EndpointEnum.login.value, json=data)
    assert response.status_code == 401
    assert response.json == {"message": "Invalid password"}


def test_register(test_client: FlaskClient, session: db.session) -> None:
    """Test the register endpoint."""
    data = {
        "first_name": "Test",
        "last_name": "User",
        "username": "test_user",
        "password": "hardpass",
    }
    response = test_client.post(EndpointEnum.register.value, json=data)
    assert response.status_code == 201
    assert response.json == {"message": "User created successfully"}
    user = session.query(Users).filter(Users.username == "test_user").first()
    assert user.first_name == "Test"
    assert user.last_name == "User"
    assert user.username == "test_user"
    assert user.password is not None
    assert user.role_id == RoleEnum.student.value


def test_register_invalid_request(test_client: FlaskClient) -> None:
    """Test the register endpoint with an invalid request."""
    data = {
        "first_name": "BOB",
    }
    response = test_client.post(EndpointEnum.register.value, json=data)
    assert response.status_code == 400
    assert response.json == {"message": "Invalid request body"}


def test_register_existing_user(test_client: FlaskClient, session: db.session) -> None:
    """Test the register endpoint with an existing user."""
    data = {
        "first_name": "Test",
        "last_name": "User",
        "username": "admin",
        "password": "hardpass",
    }
    response = test_client.post(EndpointEnum.register.value, json=data)
    assert response.status_code == 409
    assert response.json == {"message": "Username already exists"}
