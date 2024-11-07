import pytest
import requests
from tests.utils.test_utils import (
    BASE_URL,
    register_user,
    add_reminder,
    delete_reminder,
    generate_random_email,
    generate_random_date,
)

# ------------------------------------------------------------------------------------------------------------

# Tests for the reminder deletion endpoint


# Error test - missing email parameter in the query
def test_reminder_delete_missing_email():
    response = requests.delete(f"{BASE_URL}/delete/reminder")
    # Expecting a 400 status code for missing email parameter
    assert (
        response.status_code == 400
    ), f"Expected 400 for missing email parameter, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "The 'email' parameter is required." in json_response["detail"]


# Error test - non-existent email
def test_reminder_delete_nonexistent_email():
    params = {"email": "nonexistent@example.com"}
    response = delete_reminder(params)
    # Expecting a 404 status code when the email doesn't exist
    assert (
        response.status_code == 404
    ), f"Expected 404 for nonexistent email, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Email not found" in json_response["detail"]


# Error test - invalid email format
def test_reminder_delete_invalid_email_format():
    params = {"email": "invalidemailformat"}
    response = delete_reminder(params)
    # Expecting a 400 status code for invalid email format
    assert (
        response.status_code == 400
    ), f"Expected 400 for invalid email format, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert (
        "The email must be in the format 'name@domain.com' or 'name@domain.br'."
        in json_response["detail"]
    )


# Success test - deleting reminder with a valid email
def test_reminder_delete_success():
    # Register a user to test reminder deletion
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "Registration failed during the delete reminder test."

    # Reminder data to be added
    date = generate_random_date()
    data = {
        "email_id": email,
        "item_type": "Loan Payment",
        "value": 500.00,
        "annotation": "October installment",
        "date": date,
    }
    response = add_reminder(data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    json_response = response.json()
    assert "message" in json_response
    assert "Reminder added successfully" in json_response["message"]

    # Valid key for deletion
    params = {"email": email}
    response = delete_reminder(params)
    # Expecting a 200 status code for successful reminder deletion
    assert (
        response.status_code == 200
    ), f"Expected 200 for successful revenue deletion, got {response.status_code}"
    json_response = response.json()
    assert "message" in json_response
    assert "Reminder deleted successfully." in json_response["message"]


# Test for disallowed methods (POST, PUT, GET, PATCH)
@pytest.mark.parametrize("method", ["post", "put", "get", "patch"])
def test_reminder_delete_disallowed_methods(method):
    response = getattr(requests, method)(f"{BASE_URL}/delete/reminder")
    # Expecting a 405 status code for disallowed methods
    assert (
        response.status_code == 405
    ), f"Expected 405 for {method.upper()}, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]
