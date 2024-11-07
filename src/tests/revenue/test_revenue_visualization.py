import pytest
import requests
from tests.utils.test_utils import (
    BASE_URL,
    register_user,
    add_revenue,
    visualize_revenue,
    generate_random_email,
    generate_random_date,
)

# ------------------------------------------------------------------------------------------------------------

# Tests for the revenue visualization endpoint


# Error test - missing email query parameter
def test_revenue_visualization_missing_email():
    # Test if the server responds with 400 when the 'email' parameter is missing
    response = requests.get(f"{BASE_URL}/visualization/revenue")
    assert (
        response.status_code == 400
    ), f"Expected 400 for missing email parameter, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "The 'email' parameter is required." in json_response["detail"]


# Error test - nonexistent email
def test_revenue_visualization_nonexistent_email():
    # Test if the server responds with 404 when the provided email does not exist
    params = {"email": "nonexistent@example.com"}
    response = visualize_revenue(params)
    assert (
        response.status_code == 404
    ), f"Expected 404 for nonexistent email, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Email not found" in json_response["detail"]


# Error test - invalid email format
def test_revenue_visualization_invalid_email_format():
    # Test if the server responds with 400 when the email format is invalid
    params = {"email": "invalidemailformat"}
    response = visualize_revenue(params)
    assert (
        response.status_code == 400
    ), f"Expected 400 for invalid email format, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert (
        "The email must be in the format 'name@domain.com' or 'name@domain.br'."
        in json_response["detail"]
    )


# Success test - revenue visualization with a valid email
def test_revenue_visualization_success():
    # Register a user to test the revenue visualization
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "Registration failed during the visualization test."

    # Add revenue data
    date = generate_random_date()
    data = {
        "email_id": email,
        "item_type": "Salário",
        "value": 5000.00,
        "annotation": "Outubro",
        "date": date,
    }
    response = add_revenue(data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    json_response = response.json()
    assert "message" in json_response
    assert "Revenue added successfully" in json_response["message"]

    # Valid email for visualization
    params = {"email": email}
    response = visualize_revenue(params)
    assert (
        response.status_code == 200
    ), f"Expected 200 for successful revenue visualization, got {response.status_code}"
    json_response = response.json()
    assert "revenues" in json_response
    # Check if the 'revenues' field is a list (it is assumed that the API returns a list of revenues)
    assert isinstance(
        json_response["revenues"], list
    ), "Expected revenues to be a list."


# Test for disallowed HTTP methods
@pytest.mark.parametrize("method", ["post", "put", "delete", "patch"])
def test_revenue_visualization_disallowed_methods(method):
    # Test if the server responds with 405 for disallowed HTTP methods
    response = getattr(requests, method)(f"{BASE_URL}/visualization/revenue")
    assert (
        response.status_code == 405
    ), f"Expected 405 for {method.upper()}, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]
