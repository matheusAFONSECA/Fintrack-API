import pytest
import requests
from tests.utils.test_utils import (
    BASE_URL,
    register_user,
    add_alert,
    generate_random_email,
    generate_random_date,
)


# -------------------------------------------------------------------------------------------------
# Tests for the alert addition endpoint


# Test - Invalid email format
def test_add_reminder_invalid_email():
    """
    Tests alert addition with an invalid email format.
    """
    date = generate_random_date()
    data = {
        "email_id": "matheusfonseca",  # Invalid email format
        "item_type": "Loan Payment",
        "value": 500.00,
        "annotation": "October installment",
        "date": date,
    }
    response = add_alert(data)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert (
        "The email must be in the format 'name@domain.com' or 'name@domain.br'."
        in json_response["detail"]
    )


# Test - Alert addition with a non-existent email
def test_add_alert_nonexistent_email():
    """
    Tests alert addition with a non-existent email.
    """
    add_alert_data = {
        "email_id": "nao_existe@example.com",
        "item_type": "Negative Balance",
        "value": 50.00,
        "annotation": "Alert for a non-existent email",
        "date": generate_random_date(),
    }
    add_alert_response = add_alert(add_alert_data)
    assert (
        add_alert_response.status_code == 404
    ), f"Expected 404, got {add_alert_response.status_code}"


# Test - Alert addition with a negative value
def test_add_alert_negative_value():
    """
    Tests alert addition with a negative value, which is not allowed.
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

    date = generate_random_date()
    add_alert_data = {
        "email_id": email,
        "item_type": "Negative Balance",
        "value": -50.00,  # Negative value
        "annotation": "Invalid negative value",
        "date": date,
    }
    add_alert_response = add_alert(add_alert_data)
    assert (
        add_alert_response.status_code == 400
    ), f"Expected 400, got {add_alert_response.status_code}"


# Test - Alert addition without a date
def test_add_alert_missing_date():
    """
    Tests alert addition without a date, which is a required field.
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

    add_alert_data = {
        "email_id": email,
        "item_type": "Negative Balance",
        "value": 50.00,
        "annotation": "Alert without a date",
    }
    add_alert_response = add_alert(add_alert_data)
    assert (
        add_alert_response.status_code == 400
    ), f"Expected 400, got {add_alert_response.status_code}"


# Test - Alert addition with a zero value
def test_add_alert_zero_value():
    """
    Tests alert addition with a zero value, which is not permitted.
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
    ), "Registration failed for zero value test."

    date = generate_random_date()
    add_alert_data = {
        "email_id": email,
        "item_type": "Negative Balance",
        "value": 0.00,  # Zero value
        "annotation": "Zero limit",
        "date": date,
    }
    add_alert_response = add_alert(add_alert_data)
    assert (
        add_alert_response.status_code == 400
    ), f"Expected 400, got {add_alert_response.status_code}"


# Test - Successful alert addition
def test_add_alert_success():
    """
    Tests successful alert addition with valid data.
    """
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "password123",
    }
    register_response = register_user(register_data)
    assert register_response.status_code == 200, "Registration failed for success test."

    date = generate_random_date()
    add_alert_data = {
        "email_id": email,
        "item_type": "Negative Balance",
        "value": 50.00,
        "annotation": "Balance below limit",
        "date": date,
    }
    add_alert_response = add_alert(add_alert_data)
    assert (
        add_alert_response.status_code == 200
    ), f"Expected 200, got {add_alert_response.status_code}"


# Test - Disallowed methods on the alert endpoint
@pytest.mark.parametrize("method", ["get", "put", "delete", "patch"])
def test_register_disallowed_methods(method):
    """
    Tests disallowed HTTP methods (GET, PUT, DELETE, PATCH) on the alert endpoint.
    """
    response = getattr(requests, method)(f"{BASE_URL}/add/alert")
    assert (
        response.status_code == 405
    ), f"Expected 405 for {method.upper()}, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]
