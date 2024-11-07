import pytest
import requests
from tests.utils.test_utils import (
    BASE_URL,
    register_user,
    add_reminder,
    delete_reminder,
    generate_random_email,
    generate_random_date,
)

# ------------------------------------------------------------------------------------------------------------

# Testes com o endpoint de visualização de lembretess


# Teste de erro - chave de consulta ausente
def test_reminder_delete_missing_email():
    response = requests.delete(f"{BASE_URL}/delete/reminder")
    assert (
        response.status_code == 400
    ), f"Expected 400 for missing email parameter, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "The 'email' parameter is required." in json_response["detail"]


# Teste de erro - e-mail inexistente
def test_reminder_delete_nonexistent_email():
    params = {"email": "nonexistent@example.com"}
    response = delete_reminder(params)
    assert (
        response.status_code == 404
    ), f"Expected 404 for nonexistent email, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Email not found" in json_response["detail"]


# Teste de erro - formato de e-mail inválido
def test_reminder_delete_invalid_email_format():
    params = {"email": "invalidemailformat"}
    response = delete_reminder(params)
    assert (
        response.status_code == 400
    ), f"Expected 400 for invalid email format, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert (
        "The email must be in the format 'name@domain.com' or 'name@domain.br'."
        in json_response["detail"]
    )


# Teste de sucesso - visualização de alertas com e-mail válido
def test_reminder_delete_success():
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
    ), "Registro falhou durante o teste deletar alertas."

    # Dados de lembrete
    date = generate_random_date()
    data = {
        "email_id": email,
        "item_type": "Pagamento de Empréstimo",
        "value": 500.00,
        "annotation": "Parcela de outubro",
        "date": date
    }
    response = add_reminder(data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    json_response = response.json()
    assert "message" in json_response
    assert "Reminder added successfully" in json_response["message"]

    # Chave para deletar válida
    params = {"email": email}
    response = delete_reminder(params)
    assert (
        response.status_code == 200
    ), f"Expected 200 for successful revenue deletion, got {response.status_code}"
    json_response = response.json()
    assert "message" in json_response
    assert (
        "Reminder deleted successfully."
        in json_response["message"]
    )


# Teste de método não permitido
@pytest.mark.parametrize("method", ["post", "put", "get", "patch"])
def test_reminder_delete_disallowed_methods(method):
    response = getattr(requests, method)(f"{BASE_URL}/delete/reminder")
    assert (
        response.status_code == 405
    ), f"Expected 405 for {method.upper()}, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]
