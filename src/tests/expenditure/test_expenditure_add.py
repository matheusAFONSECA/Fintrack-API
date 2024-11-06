import pytest
import requests
from tests.utils.test_utils import (
    BASE_URL,
    register_user,
    add_expenditure,
    generate_random_email,
    generate_random_date,
)

# ------------------------------------------------------------------------------------------------------------

# Testes com o endpoint de adicionar despesa


# Teste de erro - adição de despesa com valor negativo
def test_add_expenditure_negative_value():
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert register_response.status_code == 200, "Registro falhou no teste de valor negativo."

    date = generate_random_date()
    data = {
        "email_id": email,
        "item_type": "Supermercado",
        "value": -200.00,
        "annotation": "Valor negativo inválido",
        "date": date,
    }
    response = add_expenditure(data)
    assert response.status_code == 400, f"Expected status 400 for negative value, got {response.status_code}"

# Teste de erro - adição de despesa com valor zero
def test_add_expenditure_zero_value():
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert register_response.status_code == 200, "Registro falhou no teste de valor zero."

    date = generate_random_date()
    data = {
        "email_id": email,
        "item_type": "Supermercado",
        "value": 0.00,
        "annotation": "Valor zero",
        "date": date,
    }
    response = add_expenditure(data)
    assert response.status_code == 400, f"Expected status 400 for zero value, got {response.status_code}"

# Teste de erro - data inválida
def test_add_expenditure_invalid_date():
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert register_response.status_code == 200, "Registro falhou no teste sem data."

    data = {
        "email_id": email,
        "item_type": "Supermercado",
        "value": 200.00,
        "annotation": "Compra de outubro",
    }
    response = add_expenditure(data)
    assert response.status_code == 400, f"Expected status 400 for missing date, got {response.status_code}"

# Teste de erro - adição de despesa com e-mail inexistente
def test_add_expenditure_nonexistent_email():
    data = {
        "email_id": "nao_existe@example.com",
        "item_type": "Supermercado",
        "value": 200.00,
        "annotation": "Compra de outubro",
        "date": generate_random_date(),
    }
    response = add_expenditure(data)
    assert response.status_code == 404, f"Expected status 404 for nonexistent email, got {response.status_code}"

# Teste de erro - email inválido
def test_add_expenditure_invalid_email():
    date = generate_random_date()
    data = {
        "email_id": "matheusfonseca",  # Email sem formato válido
        "item_type": "Supermercado",
        "value": 200.00,
        "annotation": "Compra de outubro",
        "date": date
    }
    response = add_expenditure(data)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "The email must be in the format 'name@domain.com' or 'name@domain.br'." in json_response["detail"]

# Teste de sucesso - despesa válida
def test_add_expenditure_success():
    # Registro de um usuário para testar a adição da despesa
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert register_response.status_code == 200, "Registro falhou durante o teste de adição de despesa."

    # Dados de despesa
    date = generate_random_date()
    data = {
        "email_id": email,
        "item_type": "Supermercado",
        "value": 200.00,
        "annotation": "Compra de outubro",
        "date": date
    }
    response = add_expenditure(data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    json_response = response.json()
    assert "message" in json_response
    assert "Expenditure added successfully" in json_response["message"]

# Teste de método não permitido
@pytest.mark.parametrize("method", ["get", "put", "delete", "patch"])
def test_add_expenditure_disallowed_methods(method):
    response = getattr(requests, method)(f"{BASE_URL}/add/expenditure")
    assert response.status_code == 405, f"Expected 405 for {method.upper()}, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]
