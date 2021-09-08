import pytest
import json

from api import app

"""
   Sample test data
"""

DUMMY_USERNAME = "apple"
DUMMY_EMAIL = "apple@apple.com"
DUMMY_PASS = "newpassword" 

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

class TestUserAPI:
    def test_user_signup(self, client):
        """
           Tests /api/users/register API
        """
        response = client.post(
            "/api/users/register",
            data=json.dumps(
                {
                    "username": DUMMY_USERNAME,
                    "email": DUMMY_EMAIL,
                    "password": DUMMY_PASS
                }
            ),
            content_type="application/json"
        )

        data = json.loads(response.data.decode())
        assert response.status_code == 200
        assert "The user was successfully registered" in data["msg"]

    def test_user_signup_invalid_data(self, client):
        """
           Tests /api/users/register API: invalid data like email field empty
        """
        response = client.post(
            "/api/users/register",
            data=json.dumps(
                {
                    "username": DUMMY_USERNAME,
                    "email": "",
                    "password": DUMMY_PASS
                }
            ),
            content_type="application/json"
        )

        data = json.loads(response.data.decode())
        assert response.status_code == 400
        assert "'' is too short" in data["msg"]

    def test_user_login_correct(self, client):
        """
           Tests /api/users/login API: Correct credentials
        """
        response = client.post(
            "/api/users/login",
            data=json.dumps(
                {
                    "email": DUMMY_EMAIL,
                    "password": DUMMY_PASS
                }
            ),
            content_type="application/json"
        )

        data = json.loads(response.data.decode())
        assert response.status_code == 200
        assert data["token"] != ""

    def test_user_login_error(self, client):
        """
           Tests /api/users/login API: Wrong credentials
        """
        response = client.post(
            "/api/users/login",
            data=json.dumps(
                {
                    "email": DUMMY_EMAIL,
                    "password": DUMMY_EMAIL
                }
            ),
            content_type="application/json"
        )

        data = json.loads(response.data.decode())
        assert response.status_code == 400
        assert "Wrong credentials." in data["msg"]
