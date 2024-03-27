from flask.testing import FlaskClient
from flask_jwt_extended import get_jwt_identity
from werkzeug.test import TestResponse

from src.app import db
from src.app.models.roles import RoleEnum
from src.app.models.users import Users
from tests.conftest import EndpointEnum


def get_token(test_client: FlaskClient) -> str:
    """Get the token for the admin user."""
    response = test_client.post(
        EndpointEnum.login.value, json={"username": "admin", "password": "hardpass"}
    )
    return response.json["access_token"]
def get_admin_login() -> dict:
    return {"username": "admin", "password": "hardpass"}


def register_user(test_client: FlaskClient, data: dict) -> TestResponse:
    """Register a user."""
    response = test_client.post(EndpointEnum.register.value, json=data)
    return response


def login_user(test_client: FlaskClient, data: dict) -> TestResponse:
    """Login the user."""
    response = test_client.post(EndpointEnum.login.value, json=data)
    return response


def get_token(test_client: FlaskClient, data: dict) -> str:
    """Get the token for a user."""
    return login_user(test_client, data).json["access_token"]


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


def test_get_user_by_id(test_client: FlaskClient, session: db.session) -> None:
    """Test the get user by id endpoint."""
    response = test_client.get(
        EndpointEnum.get_user.value.format(user_id=1),
        headers={"Authorization": f"Bearer {get_token(test_client)}"},
    )
    assert response.status_code == 200
    assert response.json["id"] == 1
    assert response.json["username"] == "admin"
    assert response.json["role_id"] == RoleEnum.admin.value


def test_get_user_by_id_user_not_found(test_client: FlaskClient) -> None:
    """Test the get user by id endpoint with a user not found."""
    response = test_client.get(
        EndpointEnum.get_user.value.format(user_id=69420),
        headers={"Authorization": f"Bearer {get_token(test_client)}"},
    )
    assert response.status_code == 404
    assert response.json == {"message": "User not found"}


def test_get_all_users(test_client: FlaskClient) -> None:
    """Test the get all users endpoint."""
    response = test_client.get(
        EndpointEnum.get_all_users.value,
    )
    assert response.status_code == 200
    admin = response.json[0]
    assert admin["id"] == 1
    assert admin["username"] == "admin"
    assert admin["role_id"] == RoleEnum.admin.value
    assert len(response.json) >= 1
def test_update_user(test_client: FlaskClient, session: db.session) -> None:
    """Test the update user endpoint."""
    # Update all fields
    data = {
        "first_name": "Changed",
        "last_name": "Name",
        "gpa": 3.2,
        "academic_year": "Junior",
        "github_link": "www.github.com/profile",
        "linkedin_link": "www.linkedin.com/profile",
        "website_link": "www.uwu.com",
        "profile_picture_link": "www.owo.com",
        "email": "changed@muic.edu",
        "phone_number": "011-456-7881",
        "description": "Knock, knock. Who's there? Just me. Just me who? Just me, I'm updated.",
        "internship_time_period_id": 1,
    }

    response = test_client.put(
        EndpointEnum.edit_profile.value,
        json=data,
        headers={
            "Authorization": f"Bearer {get_token(test_client, get_admin_login())}"
        },
    )

    assert response.status_code == 200
    assert response.json == {"message": "User profile updated successfully"}
    user = session.query(Users).filter(Users.id == get_jwt_identity()).first()
    assert user.first_name == "Changed"
    assert user.last_name == "Name"
    assert user.gpa == 3.2
    assert user.academic_year == "Junior"
    assert user.github_link == "www.github.com/profile"
    assert user.linkedin_link == "www.linkedin.com/profile"
    assert user.website_link == "www.uwu.com"
    assert user.profile_picture_link == "www.owo.com"
    assert user.email == "changed@muic.edu"
    assert user.phone_number == "011-456-7881"
    assert (
        user.description
        == "Knock, knock. Who's there? Just me. Just me who? Just me, I'm updated."
    )
    assert user.internship_time_period_id == 1

    # Another user
    register_user(
        test_client,
        {
            "first_name": "Second",
            "last_name": "User",
            "username": "MeToo",
            "password": "twice",
        },
    )

    user2_login = {"username": "MeToo", "password": "twice"}

    response = test_client.put(
        EndpointEnum.edit_profile.value,
        json=data,
        headers={"Authorization": f"Bearer {get_token(test_client, user2_login)}"},
    )

    data = {
        "first_name": "Second",
        "last_name": "Name",
        "gpa": 4.0,
        "academic_year": "Freshman",
        "github_link": "www.github.com/MeToo",
        "linkedin_link": "www.linkedin.com/MeToo",
        "website_link": "www.MeToo.com",
        "profile_picture_link": "www.imgur.com",
        "email": "MeToo@student.mahidol.edu",
        "phone_number": "100-000-000",
        "description": "Too B or not too B?",
        "internship_time_period_id": 1,
    }


def test_update_user_invalid_request(test_client: FlaskClient) -> None:
    data = {
        "first_name": "Changed",
    }
    response = test_client.put(
        EndpointEnum.edit_profile.value,
        json=data,
        headers={
            "Authorization": f"Bearer {get_token(test_client, get_admin_login())}"
        },
    )

    assert response.status_code == 400
    assert response.json == {"message": "Invalid request body"}
