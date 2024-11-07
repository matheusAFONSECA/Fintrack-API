import pytest
import requests
from tests.utils.test_utils import (
    BASE_URL,
    register_user,
    add_revenue,
    update_revenue,
    generate_random_email,
    generate_random_date,
)

# ------------------------------------------------------------------------------------------------------------

# Tests for the revenue update endpoint


def test_revenue_update_missing_email():
    """
    Test that the API returns a 400 status code if the 'email' parameter is missing when trying to update a revenue entry.

    This test sends a PUT request to the /update/revenue endpoint without the 'email' parameter.
    It verifies that the API responds with a 400 status code and an appropriate error message.
    """
    data = {
        "type": "Salário Atualizado",
        "value": 5200.00,
        "annotation": "Receita atualizada para outubro",
        "date": "2024-10-31",
    }
    response = requests.put(f"{BASE_URL}/update/revenue", json=data)
    assert (
        response.status_code == 400
    ), f"Expected 400 for missing email parameter, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "The 'email' parameter is required." in json_response["detail"]


def test_revenue_update_nonexistent_email():
    """
    Test that the API returns a 404 status code if an attempt is made to update a revenue entry with a non-existent email.

    This test sends a PUT request to the /update/revenue endpoint with an email that does not exist in the database.
    It verifies that the API responds with a 404 status code and an appropriate error message.
    """
    params = {"email": "nonexistent@example.com"}
    data = {
        "type": "Salário Atualizado",
        "value": 5200.00,
        "annotation": "Receita atualizada para outubro",
        "date": "2024-10-31",
    }
    response = update_revenue(params, data)
    assert (
        response.status_code == 404
    ), f"Expected 404 for nonexistent email, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Email not found" in json_response["detail"]


def test_revenue_update_invalid_email_format():
    """
    Test that the API returns a 400 status code if an invalid email format is provided when attempting to update a revenue entry.

    This test sends a PUT request to the /update/revenue endpoint with an improperly formatted email.
    It verifies that the API responds with a 400 status code and an appropriate error message about email format.
    """
    params = {"email": "invalidemailformat"}
    data = {
        "type": "Salário Atualizado",
        "value": 5200.00,
        "annotation": "Receita atualizada para outubro",
        "date": "2024-10-31",
    }
    response = update_revenue(params, data)
    assert (
        response.status_code == 400
    ), f"Expected 400 for invalid email format, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert (
        "The email must be in the format 'name@domain.com' or 'name@domain.br'."
        in json_response["detail"]
    )


def test_revenue_update_success():
    """
    Test successful update of a revenue entry after registering a user and adding a revenue entry.

    This test registers a user, adds a revenue entry associated with the user's email, and then updates the revenue entry.
    It verifies that the API responds with a 200 status code and a success message.
    """
    # Register a user to test update of revenue
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "User registration failed during revenue update test."

    # Add revenue data for updating
    date = generate_random_date()
    data = {
        "email_id": email,
        "item_type": "Salário",
        "value": 5000.00,
        "annotation": "Initial salary",
        "date": date,
    }
    add_response = add_revenue(data)
    assert (
        add_response.status_code == 200
    ), f"Expected 200, got {add_response.status_code}"

    # Update revenue
    update_data = {
        "type": "Salário Atualizado",
        "value": 5200.00,
        "annotation": "Receita atualizada para outubro",
        "date": date,
    }
    params = {"email": email}
    response = update_revenue(params, update_data)
    assert (
        response.status_code == 200
    ), f"Expected 200 for successful revenue update, got {response.status_code}"
    json_response = response.json()
    assert json_response["message"] == "Revenue updated successfully!"


@pytest.mark.parametrize("method", ["post", "delete", "get", "patch"])
def test_revenue_update_disallowed_methods(method):
    """
    Test that the API returns a 405 status code for HTTP methods that are not allowed for the update revenue endpoint.

    This test sends requests with disallowed HTTP methods to the /update/revenue endpoint.
    It verifies that the API responds with a 405 status code and an appropriate error message.
    """
    response = getattr(requests, method)(f"{BASE_URL}/update/revenue")
    assert (
        response.status_code == 405
    ), f"Expected 405 for {method.upper()}, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]
