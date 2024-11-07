import pytest
import requests
from tests.utils.test_utils import (
    BASE_URL,
    register_user,
    add_expenditure,
    generate_random_email,
    generate_random_date,
)

# ------------------------------------------------------------------------------------------------------------

# Tests for the expenditure addition endpoint


# Error Test - Adding expenditure with a negative value
def test_add_expenditure_negative_value():
    """
    Tests that adding an expenditure with a negative value returns a 400 status.
    """
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "User registration failed in negative value test."

    date = generate_random_date()
    data = {
        "email_id": email,
        "item_type": "Supermarket",
        "value": -200.00,
        "annotation": "Invalid negative value",
        "date": date,
    }
    response = add_expenditure(data)
    assert (
        response.status_code == 400
    ), f"Expected status 400 for negative value, got {response.status_code}"


# Error Test - Adding expenditure with zero value
def test_add_expenditure_zero_value():
    """
    Tests that adding an expenditure with a value of zero returns a 400 status.
    """
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "User registration failed in zero value test."

    date = generate_random_date()
    data = {
        "email_id": email,
        "item_type": "Supermarket",
        "value": 0.00,
        "annotation": "Zero value",
        "date": date,
    }
    response = add_expenditure(data)
    assert (
        response.status_code == 400
    ), f"Expected status 400 for zero value, got {response.status_code}"


# Error Test - Invalid date
def test_add_expenditure_invalid_date():
    """
    Tests that adding an expenditure without a date returns a 400 status.
    """
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "User registration failed in date absence test."

    data = {
        "email_id": email,
        "item_type": "Supermarket",
        "value": 200.00,
        "annotation": "October purchase",
    }
    response = add_expenditure(data)
    assert (
        response.status_code == 400
    ), f"Expected status 400 for missing date, got {response.status_code}"


# Error Test - Adding expenditure with a nonexistent email
def test_add_expenditure_nonexistent_email():
    """
    Tests that adding an expenditure with a nonexistent email returns a 404 status.
    """
    data = {
        "email_id": "nonexistent@example.com",
        "item_type": "Supermarket",
        "value": 200.00,
        "annotation": "October purchase",
        "date": generate_random_date(),
    }
    response = add_expenditure(data)
    assert (
        response.status_code == 404
    ), f"Expected status 404 for nonexistent email, got {response.status_code}"


# Error Test - Invalid email format
def test_add_expenditure_invalid_email():
    """
    Tests that adding an expenditure with an invalid email format returns a 400 status.
    """
    date = generate_random_date()
    data = {
        "email_id": "invalidemail",  # Email without a valid format
        "item_type": "Supermarket",
        "value": 200.00,
        "annotation": "October purchase",
        "date": date,
    }
    response = add_expenditure(data)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert (
        "The email must be in the format 'name@domain.com' or 'name@domain.br'."
        in json_response["detail"]
    )


# Success Test - Valid expenditure addition
def test_add_expenditure_success():
    """
    Tests that adding a valid expenditure successfully returns a 200 status.
    """
    # Register a user to test expenditure addition
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "User registration failed during expenditure addition test."

    # Expenditure data
    date = generate_random_date()
    data = {
        "email_id": email,
        "item_type": "Supermarket",
        "value": 200.00,
        "annotation": "October purchase",
        "date": date,
    }
    response = add_expenditure(data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    json_response = response.json()
    assert "message" in json_response
    assert "Expenditure added successfully" in json_response["message"]


# Test disallowed methods
@pytest.mark.parametrize("method", ["get", "put", "delete", "patch"])
def test_add_expenditure_disallowed_methods(method):
    """
    Tests that HTTP methods other than POST return a 405 status for the expenditure addition endpoint.
    """
    response = getattr(requests, method)(f"{BASE_URL}/add/expenditure")
    assert (
        response.status_code == 405
    ), f"Expected 405 for {method.upper()}, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]
