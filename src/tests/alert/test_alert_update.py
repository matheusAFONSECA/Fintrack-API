import pytest
import requests
from tests.utils.test_utils import (
    BASE_URL,
    generate_random_date,
    add_alert,
    register_user,
    update_alert,
    generate_random_email,
)

# -------------------------------------------------------------------------------------------------
# Tests for the alert update endpoint


def test_alert_update_missing_email():
    """
    Test that the API returns a 400 status code if the 'email' parameter is missing
    when trying to update an alert.

    Expected:
        - Status code: 400
        - JSON response with error detail mentioning the missing 'email' parameter.
    """
    data = {
        "type": "Saldo Atualizado",
        "value": 100.00,
        "annotation": "Novo limite de alerta de saldo",
    }
    response = requests.put(f"{BASE_URL}/update/alert", json=data)
    assert (
        response.status_code == 400
    ), f"Expected 400 for missing email parameter, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "The 'email' parameter is required." in json_response["detail"]


def test_alert_update_nonexistent_email():
    """
    Test that the API returns a 404 status code if an attempt is made to update an alert
    with a non-existent email.

    Expected:
        - Status code: 404
        - JSON response with error detail mentioning that the email was not found.
    """
    params = {"email": "nonexistent@example.com"}
    data = {
        "type": "Saldo Atualizado",
        "value": 100.00,
        "annotation": "Novo limite de alerta de saldo",
    }
    response = update_alert(params, data)
    assert (
        response.status_code == 404
    ), f"Expected 404 for nonexistent email, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Email not found" in json_response["detail"]


def test_alert_update_invalid_email_format():
    """
    Test that the API returns a 400 status code if an invalid email format is provided
    when attempting to update an alert.

    Expected:
        - Status code: 400
        - JSON response with error detail mentioning the required email format.
    """
    params = {"email": "invalidemailformat"}
    data = {
        "type": "Saldo Atualizado",
        "value": 100.00,
        "annotation": "Novo limite de alerta de saldo",
    }
    response = update_alert(params, data)
    assert (
        response.status_code == 400
    ), f"Expected 400 for invalid email format, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert (
        "The email must be in the format 'name@domain.com' or 'name@domain.br'."
        in json_response["detail"]
    )


def test_alert_update_success():
    """
    Test successful update of an alert after registering a user.

    Steps:
        1. Register a new user.
        2. Add an initial alert for that user.
        3. Update the alert and verify the update was successful.

    Expected:
        - Status code: 200 for user registration, alert addition, and update.
        - JSON response with a success message upon alert update.
    """
    # Register a user to test update of alert
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "User registration failed during alert update test."

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

    # Update alert
    update_data = {
        "type": "Saldo Atualizado",
        "value": 100.00,
        "annotation": "Novo limite de alerta de saldo",
    }
    params = {"email": email}
    response = update_alert(params, update_data)
    assert (
        response.status_code == 200
    ), f"Expected 200 for successful alert update, got {response.status_code}"
    json_response = response.json()
    assert json_response["message"] == "Alert updated successfully!"


@pytest.mark.parametrize("method", ["post", "delete", "get", "patch"])
def test_alert_update_disallowed_methods(method):
    """
    Test that the API returns a 405 status code for HTTP methods that are not allowed
    for the update alert endpoint.

    Expected:
        - Status code: 405 for unsupported methods.
        - JSON response with error detail mentioning "Method Not Allowed".
    """
    response = getattr(requests, method)(f"{BASE_URL}/update/alert")
    assert (
        response.status_code == 405
    ), f"Expected 405 for {method.upper()}, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]
