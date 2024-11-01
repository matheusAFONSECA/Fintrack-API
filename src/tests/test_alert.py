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

# Testes com o endpoint de adicionar alarme


# Teste de adição de alarme com e-mail inexistente
def test_add_alert_nonexistent_email():
    # Dados de alerta para e-mail não registrado
    add_alert_data = {
        "email_id": "nao_existe@example.com",
        "item_type": "Saldo Negativo",
        "value": 50.00,
        "annotation": "Alerta para e-mail inexistente",
        "date": generate_random_date(),
    }
    add_alert_response = add_alert(add_alert_data)
    assert (
        add_alert_response.status_code == 404
    ), f"Expected status 404 for nonexistent email, got {add_alert_response.status_code}"


# Teste de adição de alarme com valor negativo
def test_add_alert_negative_value():
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "Registro falhou no teste de valor negativo."

    # Dados de alerta com valor negativo
    date = generate_random_date()
    add_alert_data = {
        "email_id": email,
        "item_type": "Saldo Negativo",
        "value": -50.00,
        "annotation": "Valor negativo inválido",
        "date": date,
    }
    add_alert_response = add_alert(add_alert_data)
    assert (
        add_alert_response.status_code == 400
    ), f"Expected status 400 for negative value, got {add_alert_response.status_code}"


# Teste de adição de alarme sem data
def test_add_alert_missing_date():
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert register_response.status_code == 200, "Registro falhou no teste sem data."

    # Dados de alerta sem data
    add_alert_data = {
        "email_id": email,
        "item_type": "Saldo Negativo",
        "value": 50.00,
        "annotation": "Alerta sem data",
    }
    add_alert_response = add_alert(add_alert_data)
    assert (
        add_alert_response.status_code == 400
    ), f"Expected status 400 for missing date, got {add_alert_response.status_code}"


# Teste de adição de alarme com valor de limite zero
def test_add_alert_zero_value():
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "Registro falhou no teste de valor zero."

    # Dados de alerta com valor zero
    date = generate_random_date()
    add_alert_data = {
        "email_id": email,
        "item_type": "Saldo Negativo",
        "value": 0.00,
        "annotation": "Limite zero",
        "date": date,
    }
    add_alert_response = add_alert(add_alert_data)
    assert (
        add_alert_response.status_code == 400
    ), f"Expected status 400 for zero value, got {add_alert_response.status_code}"


# Teste de sucesso - adição de alarme válida
def test_add_alert_success():
    # Registro de um usuário para testar a adição do alerta
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "Registro falhou durante o testar a adição do alerta."

    # Dados de alerta
    date = generate_random_date()
    add_alert_data = {
        "email_id": email,
        "item_type": "Saldo Negativo",
        "value": 50.00,
        "annotation": "Saldo abaixo do limite",
        "date": date,
    }
    add_alert_response = add_alert(add_alert_data)
    assert (
        add_alert_response.status_code == 200
    ), f"Expected status 200, got {add_alert_response.status_code}"


# Tests de métodos não permitidos
@pytest.mark.parametrize("method", ["get", "put", "delete", "patch"])
def test_register_disallowed_methods(method):
    response = getattr(requests, method)(f"{BASE_URL}/add/alert")
    assert (
        response.status_code == 405
    ), f"Expected 405 for {method.upper()}, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]
