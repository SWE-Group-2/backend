from flask.testing import FlaskClient

from src.app import db
from src.app.models.roles import RoleEnum
from src.app.models.users import Users
from tests.test_internship import get_token


def test_user_deletion(
    test_client: FlaskClient, session: db.session, access_token: str
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
        headers={"Authorization": f"Bearer {get_token(test_client)}"},
    )
    assert response.status_code == 200
    assert response.json == {"message": "User deleted successfully"}
    user = session.query(Users).filter(Users.username == "testuser").first()
    assert user is None


def test_user_deletion_invalid_request(
    test_client: FlaskClient, access_token: str
) -> None:
    """Test the user deletion endpoint with an invalid request."""
    response = test_client.delete(
        "/admin/delete_user/0",
        headers={"Authorization": f"Bearer {get_token(test_client)}"},
    )
    assert response.status_code == 404
    assert response.json == {"message": "User not found"}
