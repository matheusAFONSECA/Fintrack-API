import pytest
import requests
from tests.utils.test_utils import (
    BASE_URL,
    register_user,
    add_expenditure,
    delete_expenditure,
    generate_random_email,
    generate_random_date,
)

# ------------------------------------------------------------------------------------------------------------

# Tests for the expenditure deletion endpoint


def test_expenditure_delete_missing_email():
    """
    Test that the API returns a 400 status code if the 'email' parameter is missing when trying to delete an expenditure.
    """
    response = requests.delete(f"{BASE_URL}/delete/expenditure")
    assert (
        response.status_code == 400
    ), f"Expected 400 for missing email parameter, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "The 'email' parameter is required." in json_response["detail"]


def test_expenditure_delete_nonexistent_email():
    """
    Test that the API returns a 404 status code if an attempt is made to delete an expenditure with a non-existent email.
    """
    params = {"email": "nonexistent@example.com"}
    response = delete_expenditure(params)
    assert (
        response.status_code == 404
    ), f"Expected 404 for nonexistent email, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Email not found" in json_response["detail"]


def test_expenditure_delete_invalid_email_format():
    """
    Test that the API returns a 400 status code if an invalid email format is provided when attempting to delete an expenditure.
    """
    params = {"email": "invalidemailformat"}
    response = delete_expenditure(params)
    assert (
        response.status_code == 400
    ), f"Expected 400 for invalid email format, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert (
        "The email must be in the format 'name@domain.com' or 'name@domain.br'."
        in json_response["detail"]
    )


def test_expenditure_delete_success():
    """
    Test successful deletion of an expenditure after registering a user and adding an expenditure entry.
    """
    # Register a user to test deletion of expenditures
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "User registration failed during expenditure deletion test."

    # Add expenditure data for deletion
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

    # Valid email key for deletion
    params = {"email": email}
    response = delete_expenditure(params)
    assert (
        response.status_code == 200
    ), f"Expected 200 for successful expenditure deletion, got {response.status_code}"
    json_response = response.json()
    assert "message" in json_response
    assert "Expenditure deleted successfully." in json_response["message"]


@pytest.mark.parametrize("method", ["post", "put", "get", "patch"])
def test_expenditure_delete_disallowed_methods(method):
    """
    Test that the API returns a 405 status code for HTTP methods that are not allowed for the delete expenditure endpoint.
    """
    response = getattr(requests, method)(f"{BASE_URL}/delete/expenditure")
    assert (
        response.status_code == 405
    ), f"Expected 405 for {method.upper()}, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]
