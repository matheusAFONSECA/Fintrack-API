import pytest
import requests
from tests.utils.test_utils import (
    BASE_URL,
    register_user,
    add_reminder,
    generate_random_email,
    generate_random_date,
)

# ------------------------------------------------------------------------------------------------------------

# Tests for the add reminder endpoint


# Error test - adding reminder with negative value
def test_add_reminder_negative_value():
    # Generate a random email and register the user
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "Registration failed during negative value test."

    # Prepare data for the reminder with a negative value
    date = generate_random_date()
    data = {
        "email_id": email,
        "item_type": "Negative Balance",
        "value": -50.00,
        "annotation": "Invalid negative value",
        "date": date,
    }
    # Send the request and check for status 400
    response = add_reminder(data)
    assert (
        response.status_code == 400
    ), f"Expected status 400 for negative value, got {response.status_code}"


# Error test - adding reminder with zero value
def test_add_reminder_zero_value():
    # Generate a random email and register the user
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "Registration failed during zero value test."

    # Prepare data for the reminder with a zero value
    date = generate_random_date()
    data = {
        "email_id": email,
        "item_type": "Negative Balance",
        "value": 0.00,
        "annotation": "Zero limit",
        "date": date,
    }
    # Send the request and check for status 400
    response = add_reminder(data)
    assert (
        response.status_code == 400
    ), f"Expected status 400 for zero value, got {response.status_code}"


# Error test - invalid date
def test_add_reminder_invalid_date():
    # Generate a random email and register the user
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "Registration failed during test with no date."

    # Prepare data for the reminder with no date field
    data = {
        "email_id": email,
        "item_type": "Loan Payment",
        "value": 500.00,
        "annotation": "October installment",
    }
    # Send the request and check for status 400
    response = add_reminder(data)
    assert (
        response.status_code == 400
    ), f"Expected status 400 for missing date, got {response.status_code}"


# Error test - adding reminder with nonexistent email
def test_add_reminder_nonexistent_email():
    # Prepare data with a nonexistent email
    data = {
        "email_id": "nao_existe@example.com",
        "item_type": "Negative Balance",
        "value": 50.00,
        "annotation": "Alert for nonexistent email",
        "date": generate_random_date(),
    }
    # Send the request and check for status 404
    response = add_reminder(data)
    assert (
        response.status_code == 404
    ), f"Expected status 404 for nonexistent email, got {response.status_code}"


# Error test - invalid email format
def test_add_reminder_invalid_email():
    # Prepare data with an invalid email format
    date = generate_random_date()
    data = {
        "email_id": "matheusfonseca",  # Invalid email format
        "item_type": "Loan Payment",
        "value": 500.00,
        "annotation": "October installment",
        "date": date,
    }
    # Send the request and check for status 400
    response = add_reminder(data)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    # Verify the error message in the response
    json_response = response.json()
    assert "detail" in json_response
    assert (
        "The email must be in the format 'name@domain.com' or 'name@domain.br'."
        in json_response["detail"]
    )


# Success test - valid reminder
def test_add_reminder_success():
    # Register a user to test reminder addition
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "Registration failed during the test for adding a reminder."

    # Prepare valid reminder data
    date = generate_random_date()
    data = {
        "email_id": email,
        "item_type": "Loan Payment",
        "value": 500.00,
        "annotation": "October installment",
        "date": date,
    }
    # Send the request and check for status 200
    response = add_reminder(data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    # Verify success message in the response
    json_response = response.json()
    assert "message" in json_response
    assert "Reminder added successfully" in json_response["message"]


# Test for disallowed methods (GET, PUT, DELETE, PATCH)
@pytest.mark.parametrize("method", ["get", "put", "delete", "patch"])
def test_register_disallowed_methods(method):
    # Test for each disallowed method
    response = getattr(requests, method)(f"{BASE_URL}/add/reminder")
    assert (
        response.status_code == 405
    ), f"Expected 405 for {method.upper()}, got {response.status_code}"
    # Verify the error message for disallowed methods
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]
