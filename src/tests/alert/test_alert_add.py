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
