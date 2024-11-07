import pytest
import requests
from tests.utils.test_utils import (
    BASE_URL,
    generate_random_date,
    register_user,
    add_reminder,
    update_reminder,
    generate_random_email,
)

# ------------------------------------------------------------------------------------------------------------

# Tests for the reminder update endpoint


def test_reminder_update_missing_email():
    """
    Test that the API returns a 400 status code if the 'email' parameter is missing when trying to update a reminder.
    """
    data = {
        "type": "Pagamento Atualizado",
        "value": 1000.00,
        "annotation": "Ajuste de lembrete de pagamento",
    }
    response = requests.put(f"{BASE_URL}/update/reminder", json=data)
    assert (
        response.status_code == 400
    ), f"Expected 400 for missing email parameter, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "The 'email' parameter is required." in json_response["detail"]


def test_reminder_update_nonexistent_email():
    """
    Test that the API returns a 404 status code if an attempt is made to update a reminder with a non-existent email.
    """
    params = {"email": "nonexistent@example.com"}
    data = {
        "type": "Pagamento Atualizado",
        "value": 1000.00,
        "annotation": "Ajuste de lembrete de pagamento",
    }
    response = update_reminder(params, data)
    assert (
        response.status_code == 404
    ), f"Expected 404 for nonexistent email, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Email not found" in json_response["detail"]


def test_reminder_update_invalid_email_format():
    """
    Test that the API returns a 400 status code if an invalid email format is provided when attempting to update a reminder.
    """
    params = {"email": "invalidemailformat"}
    data = {
        "type": "Pagamento Atualizado",
        "value": 1000.00,
        "annotation": "Ajuste de lembrete de pagamento",
    }
    response = update_reminder(params, data)
    assert (
        response.status_code == 400
    ), f"Expected 400 for invalid email format, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert (
        "The email must be in the format 'name@domain.com' or 'name@domain.br'."
        in json_response["detail"]
    )


def test_reminder_update_success():
    """
    Test successful update of a reminder after registering a user and adding a reminder entry.
    """
    # Register a user to test update of reminders
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "User registration failed during reminder update test."

    # Add reminder data for updating
    date = generate_random_date()
    data = {
        "email_id": email,
        "item_type": "Loan Payment",
        "value": 500.00,
        "annotation": "October installment",
        "date": date,
    }
    add_response = add_reminder(data)
    assert (
        add_response.status_code == 200
    ), f"Expected 200, got {add_response.status_code}"

    # Update reminder
    update_data = {
        "type": "Pagamento Atualizado",
        "value": 1000.00,
        "annotation": "Ajuste de lembrete de pagamento",
    }
    params = {"email": email}
    response = update_reminder(params, update_data)
    assert (
        response.status_code == 200
    ), f"Expected 200 for successful reminder update, got {response.status_code}"
    json_response = response.json()
    assert json_response["message"] == "Reminder updated successfully!"


@pytest.mark.parametrize("method", ["post", "delete", "get", "patch"])
def test_reminder_update_disallowed_methods(method):
    """
    Test that the API returns a 405 status code for HTTP methods that are not allowed for the update reminder endpoint.
    """
    response = getattr(requests, method)(f"{BASE_URL}/update/reminder")
    assert (
        response.status_code == 405
    ), f"Expected 405 for {method.upper()}, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]
