import pytest
import requests
from tests.utils.test_utils import (
    BASE_URL,
    register_user,
    login_user,
    generate_random_email,
)


# Tests for the user login endpoint


# Success test - valid login
def test_login_success():
    # Register a user to test the login functionality
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "Registration failed during the login test."

    # Login data
    login_data = {
        "username": email,
        "password": "senha123",
    }
    login_response = login_user(login_data)
    assert (
        login_response.status_code == 200
    ), f"Expected status 200, got {login_response.status_code}"

    # Verify that the access token was returned successfully
    json_response = login_response.json()
    assert "access_token" in json_response, "Access token not found in response"
    assert (
        json_response["token_type"] == "bearer"
    ), f"Expected token type 'bearer', got {json_response['token_type']}"


# Error test - incorrect password
def test_login_invalid_password():
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert register_response.status_code == 200

    # Attempt to login with an incorrect password
    login_data = {
        "username": email,
        "password": "senha_errada",
    }
    login_response = login_user(login_data)
    assert (
        login_response.status_code == 401
    ), f"Expected status 401, got {login_response.status_code}"
    json_response = login_response.json()
    assert "detail" in json_response
    assert json_response["detail"] == "Incorrect email or password"


# Error test - unregistered user
def test_login_unregistered_user():
    # Generate a random email to ensure it is not registered
    login_data = {
        "username": generate_random_email(),
        "password": "senha123",
    }
    login_response = login_user(login_data)
    assert (
        login_response.status_code == 401
    ), f"Expected status 401, got {login_response.status_code}"
    json_response = login_response.json()
    assert "detail" in json_response
    assert json_response["detail"] == "Incorrect email or password"


# Error test - missing data (no password)
def test_login_missing_password():
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert register_response.status_code == 200

    # Attempt to login without providing a password
    login_data = {
        "username": email,
    }
    login_response = login_user(login_data)
    assert (
        login_response.status_code == 422
    ), f"Expected status 422, got {login_response.status_code}"
    json_response = login_response.json()
    assert "detail" in json_response
    assert json_response["detail"][0]["msg"] == "Field required"
    assert json_response["detail"][0]["loc"] == ["body", "password"]


# Test for disallowed HTTP methods
@pytest.mark.parametrize("method", ["get", "put", "delete", "patch"])
def test_register_disallowed_methods(method):
    # Test if the server responds with 405 for disallowed HTTP methods
    response = getattr(requests, method)(f"{BASE_URL}/user/login")
    assert (
        response.status_code == 405
    ), f"Expected 405 for {method.upper()}, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]
