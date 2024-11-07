import pytest
import requests
from tests.utils.test_utils import (
    BASE_URL,
    register_user,
    add_expenditure,
    visualize_expenditure,
    generate_random_email,
    generate_random_date,
)

# ------------------------------------------------------------------------------------------------------------

# Tests for the expenditure visualization endpoint


def test_expenditure_visualization_missing_email():
    """
    Test that the API returns a 400 status code if the 'email' parameter is missing
    when trying to visualize expenditures.
    """
    response = requests.get(f"{BASE_URL}/visualization/expenditure")
    assert (
        response.status_code == 400
    ), f"Expected 400 for missing email parameter, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "The 'email' parameter is required." in json_response["detail"]


def test_expenditure_visualization_nonexistent_email():
    """
    Test that the API returns a 404 status code if an attempt is made to visualize expenditures
    with a non-existent email.
    """
    params = {"email": "nonexistent@example.com"}
    response = visualize_expenditure(params)
    assert (
        response.status_code == 404
    ), f"Expected 404 for nonexistent email, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Email not found" in json_response["detail"]


def test_expenditure_visualization_invalid_email_format():
    """
    Test that the API returns a 400 status code if an invalid email format is provided
    when attempting to visualize expenditures.
    """
    params = {"email": "invalidemailformat"}
    response = visualize_expenditure(params)
    assert (
        response.status_code == 400
    ), f"Expected 400 for invalid email format, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert (
        "The email must be in the format 'name@domain.com' or 'name@domain.br'."
        in json_response["detail"]
    )


def test_expenditure_visualization_success():
    """
    Test successful visualization of expenditures after registering a user and adding expenditure data.
    """
    # Register a user to test expenditure visualization
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "password123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "User registration failed during expenditure visualization test."

    # Add expenditure data for visualization
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

    # Valid email key for visualization
    params = {"email": email}
    response = visualize_expenditure(params)
    assert (
        response.status_code == 200
    ), f"Expected 200 for successful expenditures visualization, got {response.status_code}"
    json_response = response.json()
    assert "expenditures" in json_response
    # Check that "expenditures" is a list (assumes the API returns a list of expenditures)
    assert isinstance(
        json_response["expenditures"], list
    ), "Expected expenditures to be a list."


@pytest.mark.parametrize("method", ["post", "put", "delete", "patch"])
def test_expenditure_visualization_disallowed_methods(method):
    """
    Test that the API returns a 405 status code for HTTP methods that are not allowed for the
    expenditure visualization endpoint.
    """
    response = getattr(requests, method)(f"{BASE_URL}/visualization/expenditure")
    assert (
        response.status_code == 405
    ), f"Expected 405 for {method.upper()}, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]
