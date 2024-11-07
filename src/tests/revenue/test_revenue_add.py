import pytest
import requests
from tests.utils.test_utils import (
    BASE_URL,
    register_user,
    add_revenue,
    generate_random_email,
    generate_random_date,
)

# ------------------------------------------------------------------------------------------------------------

# Tests for the 'add revenue' endpoint


# Test for error - trying to add revenue with a negative value
def test_add_revenue_negative_value():
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "Registration failed in the negative value test."

    date = generate_random_date()
    data = {
        "email_id": email,
        "item_type": "Salary",
        "value": -5000.00,
        "annotation": "Invalid negative value",
        "date": date,
    }
    response = add_revenue(data)
    assert (
        response.status_code == 400
    ), f"Expected status 400 for negative value, got {response.status_code}"


# Test for error - trying to add revenue with a zero value
def test_add_revenue_zero_value():
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "Registration failed in the zero value test."

    date = generate_random_date()
    data = {
        "email_id": email,
        "item_type": "Salary",
        "value": 0.00,
        "annotation": "Zero value",
        "date": date,
    }
    response = add_revenue(data)
    assert (
        response.status_code == 400
    ), f"Expected status 400 for zero value, got {response.status_code}"


# Test for error - trying to add revenue with an invalid date
def test_add_revenue_invalid_date():
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "Registration failed in the missing date test."

    data = {
        "email_id": email,
        "item_type": "Salary",
        "value": 5000.00,
        "annotation": "October",
    }
    response = add_revenue(data)
    assert (
        response.status_code == 400
    ), f"Expected status 400 for missing date, got {response.status_code}"


# Test for error - trying to add revenue with a non-existent email
def test_add_revenue_nonexistent_email():
    data = {
        "email_id": "non_existent@example.com",
        "item_type": "Salary",
        "value": 5000.00,
        "annotation": "October",
        "date": generate_random_date(),
    }
    response = add_revenue(data)
    assert (
        response.status_code == 404
    ), f"Expected status 404 for non-existent email, got {response.status_code}"


# Test for error - trying to add revenue with an invalid email format
def test_add_revenue_invalid_email():
    date = generate_random_date()
    data = {
        "email_id": "matheusfonseca",  # Invalid email format
        "item_type": "Salary",
        "value": 5000.00,
        "annotation": "October",
        "date": date,
    }
    response = add_revenue(data)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert (
        "The email must be in the format 'name@domain.com' or 'name@domain.br'."
        in json_response["detail"]
    )


# Test for success - adding a valid revenue
def test_add_revenue_success():
    # Register a user to test adding revenue
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "Registration failed during revenue addition test."

    # Revenue data
    date = generate_random_date()
    data = {
        "email_id": email,
        "item_type": "Salary",
        "value": 5000.00,
        "annotation": "October",
        "date": date,
    }
    response = add_revenue(data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    json_response = response.json()
    assert "message" in json_response
    assert "Revenue added successfully" in json_response["message"]


# Test for disallowed methods
@pytest.mark.parametrize("method", ["get", "put", "delete", "patch"])
def test_add_revenue_disallowed_methods(method):
    response = getattr(requests, method)(f"{BASE_URL}/add/revenue")
    assert (
        response.status_code == 405
    ), f"Expected 405 for {method.upper()}, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]
