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

# Testes com o endpoint de visualização de despesas


# Teste de erro - chave de consulta ausente
def test_expenditure_visualization_missing_email():
    response = requests.get(f"{BASE_URL}/visualization/expenditure")
    assert (
        response.status_code == 400
    ), f"Expected 400 for missing email parameter, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "The 'email' parameter is required." in json_response["detail"]


# Teste de erro - e-mail inexistente
def test_expenditure_visualization_nonexistent_email():
    params = {"email": "nonexistent@example.com"}
    response = visualize_expenditure(params)
    assert (
        response.status_code == 404
    ), f"Expected 404 for nonexistent email, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Email not found" in json_response["detail"]


# Teste de erro - formato de e-mail inválido
def test_expenditure_visualization_invalid_email_format():
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


# Teste de sucesso - visualização de despesas com e-mail válido
def test_expenditure_visualization_success():
    # Registro de um usuário para testar a visualização
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "Registro falhou durante o teste de visualização."

    # Dados de despesa
    date = generate_random_date()
    data = {
        "email_id": email,
        "item_type": "Supermercado",
        "value": 200.00,
        "annotation": "Compra de outubro",
        "date": date,
    }
    response = add_expenditure(data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    json_response = response.json()
    assert "message" in json_response
    assert "Expenditure added successfully" in json_response["message"]

    # Chave de visualização válida
    params = {"email": email}
    response = visualize_expenditure(params)
    assert (
        response.status_code == 200
    ), f"Expected 200 for successful expenditures visualization, got {response.status_code}"
    json_response = response.json()
    assert "expenditures" in json_response
    # Verifica se o retorno de "expenditure" é uma lista (presume-se que a API retorna uma lista de expenditures)
    assert isinstance(
        json_response["expenditures"], list
    ), "Expected expenditures to be a list."


# Teste de método não permitido
@pytest.mark.parametrize("method", ["post", "put", "delete", "patch"])
def test_expenditure_visualization_disallowed_methods(method):
    response = getattr(requests, method)(f"{BASE_URL}/visualization/expenditure")
    assert (
        response.status_code == 405
    ), f"Expected 405 for {method.upper()}, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]
