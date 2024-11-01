import pytest
import requests
from tests.utils.test_utils import (
    BASE_URL,
    register_user,
    login_user,
    add_alert,
    generate_random_email,
    generate_random_date,
)

# ------------------------------------------------------------------------------------------------------------

# Testes com o endpoint de adicionar lembretes


# Teste de método não permitido
@pytest.mark.parametrize("method", ["get", "put", "delete", "patch"])
def test_register_disallowed_methods(method):
    response = getattr(requests, method)(f"{BASE_URL}/add/reminder")
    assert (
        response.status_code == 405
    ), f"Expected 405 for {method.upper()}, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]
