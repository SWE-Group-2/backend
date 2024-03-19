from flask.testing import FlaskClient

from src.app import db
from src.app.models.roles import RoleEnum
from src.app.models.users import Users


def test_register(test_client: FlaskClient, session: db.session) -> None:
    """Test the register endpoint."""
    data = {
        "first_name": "Test",
        "last_name": "User",
        "username": "test_user",
        "password": "hardpass",
    }
    response = test_client.post("/users/register", json=data)
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
    response = test_client.post("/users/register", json=data)
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
    response = test_client.post("/users/register", json=data)
    assert response.status_code == 409
    assert response.json == {"message": "Username already exists"}
