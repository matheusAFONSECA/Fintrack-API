import uuid
import pytest
import requests
from tests.utils.test_utils import (
    BASE_URL,
    register_user,
    generate_random_email,
)

# Tests for the user registration endpoint


# Test case for invalid email format
def test_register_invalid_email_format():
    data = {
        "name": "Matheus Fonseca",
        "email": "matheusfonsecaafonso",  # Email without domain
        "password": "senha123",
    }
    response = register_user(data)
    assert (
        response.status_code == 400
    )  # Check if the status is 400 for validation error
    json_response = response.json()
    assert "detail" in json_response  # Check for "detail" field
    assert (
        "The email must be in the format 'name@domain.com' or 'name@domain.br'."
        in json_response["detail"]
    )  # Verify the correct error message


# Test case for email without domain
def test_register_email_without_domain():
    data = {
        "name": "Matheus Fonseca",
        "email": "matheus@fonseca",  # Email without a valid domain
        "password": "senha123",
    }
    response = register_user(data)
    assert (
        response.status_code == 400
    )  # Check if the status is 400 for validation error
    json_response = response.json()
    assert "detail" in json_response  # Check for "detail" field
    assert (
        "The email must be in the format 'name@domain.com' or 'name@domain.br'"
        in json_response["detail"]
    )  # Verify the correct error message


# Test case for email with an invalid domain
def test_register_email_invalid_domain():
    data = {
        "name": "Matheus Fonseca",
        "email": "matheus@domain.fake",  # Unrecognized domain
        "password": "senha123",
    }
    response = register_user(data)
    assert (
        response.status_code == 400
    )  # Check if the status is 400 for validation error
    json_response = response.json()
    assert "detail" in json_response  # Check for "detail" field
    assert (
        "The email must be in the format 'name@domain.com' or 'name@domain.br'"
        in json_response["detail"]
    )  # Verify the correct error message


# Test case for duplicate email
def test_register_duplicate_email():
    # Generate a random email to avoid conflict
    random_email = generate_random_email()

    # First registration with an email that will be duplicated
    data = {
        "name": "Matheus Fonseca",
        "email": random_email,
        "password": "senha123",
    }
    response = register_user(data)
    assert response.status_code == 200  # Check if the first registration is successful

    # Attempt to register with the same email
    response = register_user(data)
    assert (
        response.status_code == 400
    )  # Adjusted to 400 if the API returns this instead of 409
    json_response = response.json()
    assert "detail" in json_response
    assert (
        "already exists" in json_response["detail"]
    )  # Verify part of the returned message


# Test case for weak password
def test_register_weak_password():
    data = {
        "name": "Matheus Fonseca",
        "email": "matheusfonsecaafonso@gmail.com",
        "password": "123",  # Very short password
    }
    response = register_user(data)
    assert (
        response.status_code == 400
    ), f"Expected status 400, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response  # Check for "detail" field
    assert "The password must be at least 6 characters long." in json_response["detail"]


# Test case for successful registration
def test_register_success():
    # Generate a unique name and email to ensure the registration is unique
    unique_id = str(uuid.uuid4())[:8]  # Generate a short unique identifier
    data = {
        "name": f"Matheus Fonseca {unique_id}",
        "email": f"test_user_{unique_id}@gmail.com",
        "password": "senha123",
    }
    response = register_user(data)
    assert (
        response.status_code == 200
    ), f"Expected status 200, got {response.status_code}"
    json_response = response.json()
    assert "message" in json_response, "Key 'message' not found in response"
    assert (
        "successfully" in json_response["message"]
    ), f"Expected 'successfully!' in message, got {json_response['message']}"


# Test case for missing name during registration
def test_register_missing_name():
    data = {"email": "matheusfonsecaafonso@gmail.com", "password": "senha123"}
    response = register_user(data)
    assert response.status_code == 422  # Expected status code for missing data
    json_response = response.json()
    assert "detail" in json_response
    assert json_response["detail"][0]["msg"] == "Field required"
    assert json_response["detail"][0]["loc"] == ["body", "name"]


# Test case for disallowed methods on the registration endpoint
@pytest.mark.parametrize("method", ["get", "put", "delete", "patch"])
def test_register_disallowed_methods(method):
    response = getattr(requests, method)(f"{BASE_URL}/user/register")
    assert (
        response.status_code == 405
    ), f"Expected 405 for {method.upper()}, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]
