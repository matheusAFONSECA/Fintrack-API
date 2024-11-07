import pytest
import requests
from tests.utils.test_utils import (
    BASE_URL,
    register_user,
    update_alert,
    generate_random_email,
    generate_random_date,
)

# -------------------------------------------------------------------------------------------------
# Tests for the alert update endpoint


# Test - Update alert with non-existent email
def test_update_alert_nonexistent_email():
    """
    Tests updating an alert with a non-existent email.

    Expected outcome:
        The server should return a 422 status code, indicating the email is invalid.

    Assertions:
        - Status code is 422.
    """
    update_data = {
        "email_id": "nonexistent@example.com",
        "type": "Negative Balance",
        "value": 50.00,
        "annotation": "Update for non-existent email",
        "date": generate_random_date(),
    }
    response = update_alert(update_data)
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"


# Test - Update alert with a negative value
def test_update_alert_negative_value():
    """
    Tests updating an alert with a negative value, which is not allowed.

    Setup:
        - Register a new user to generate a valid email for the test.

    Expected outcome:
        The server should return a 422 status code, indicating the value is invalid.

    Assertions:
        - Registration status code is 200.
        - Update alert status code is 422.
    """
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "password123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "Registration failed for negative value test."

    update_data = {
        "email_id": email,
        "type": "Negative Balance",
        "value": -50.00,  # Negative value
        "annotation": "Invalid negative value",
        "date": generate_random_date(),
    }
    response = update_alert(update_data)
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"


# Test - Update alert without a date
def test_update_alert_missing_date():
    """
    Tests updating an alert without a date, which is a required field.

    Setup:
        - Register a new user to generate a valid email for the test.

    Expected outcome:
        The server should return a 422 status code, indicating the date field is missing.

    Assertions:
        - Registration status code is 200.
        - Update alert status code is 422.
    """
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "password123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "Registration failed for missing date test."

    update_data = {
        "email_id": email,
        "type": "Negative Balance",
        "value": 50.00,
        "annotation": "Alert without a date",
    }
    response = update_alert(update_data)
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"


# Test - Disallowed methods on the alert update endpoint
@pytest.mark.parametrize("method", ["get", "post", "delete", "patch"])
def test_update_alert_disallowed_methods(method):
    """
    Tests disallowed HTTP methods (GET, POST, DELETE, PATCH) on the alert update endpoint.

    Expected outcome:
        The server should return a 405 status code for each disallowed method.

    Assertions:
        - Status code is 405.
        - Response contains a "detail" field indicating "Method Not Allowed".
    """
    response = getattr(requests, method)(f"{BASE_URL}/update/alert")
    assert (
        response.status_code == 405
    ), f"Expected 405 for {method.upper()}, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]
