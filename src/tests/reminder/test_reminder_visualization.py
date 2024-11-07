import pytest
import requests
from tests.utils.test_utils import (
    BASE_URL,
    register_user,
    add_reminder,
    visualize_reminder,
    generate_random_email,
    generate_random_date,
)

# ------------------------------------------------------------------------------------------------------------

# Tests for the reminder visualization endpoint


# Error test - missing email parameter in the query
def test_reminder_visualization_missing_email():
    response = requests.get(f"{BASE_URL}/visualization/reminder")
    # Expecting a 400 status code for missing email parameter
    assert (
        response.status_code == 400
    ), f"Expected 400 for missing email parameter, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "The 'email' parameter is required." in json_response["detail"]


# Error test - non-existent email
def test_reminder_visualization_nonexistent_email():
    params = {"email": "nonexistent@example.com"}
    response = visualize_reminder(params)
    # Expecting a 404 status code when the email doesn't exist
    assert (
        response.status_code == 404
    ), f"Expected 404 for nonexistent email, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Email not found" in json_response["detail"]


# Error test - invalid email format
def test_reminder_visualization_invalid_email_format():
    params = {"email": "invalidemailformat"}
    response = visualize_reminder(params)
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


# Success test - visualizing reminders with a valid email
def test_reminder_visualization_success():
    # Register a user to test reminder visualization
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "Registration failed during the visualization test."

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

    # Valid visualization key
    params = {"email": email}
    response = visualize_reminder(params)
    # Expecting a 200 status code for successful reminder visualization
    assert (
        response.status_code == 200
    ), f"Expected 200 for successful reminders visualization, got {response.status_code}"
    json_response = response.json()
    assert "reminders" in json_response
    # Check if the "reminders" field is a list (assuming the API returns a list of reminders)
    assert isinstance(
        json_response["reminders"], list
    ), "Expected reminders to be a list."


# Test for disallowed methods (POST, PUT, DELETE, PATCH)
@pytest.mark.parametrize("method", ["post", "put", "delete", "patch"])
def test_reminder_visualization_disallowed_methods(method):
    response = getattr(requests, method)(f"{BASE_URL}/visualization/reminder")
    # Expecting a 405 status code for disallowed methods
    assert (
        response.status_code == 405
    ), f"Expected 405 for {method.upper()}, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]
