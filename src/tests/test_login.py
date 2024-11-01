import pytest
import requests
from tests.utils.test_utils import (
    BASE_URL,
    register_user,
    login_user,
    generate_random_email,
)


# Testes com o endpoint de login de usuário


# Teste de sucesso - login válido
def test_login_success():
    # Registro de um usuário para testar o login
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert (
        register_response.status_code == 200
    ), "Registro falhou durante o teste de login."

    # Dados de login
    login_data = {
        "username": email,
        "password": "senha123",
    }
    login_response = login_user(login_data)
    assert (
        login_response.status_code == 200
    ), f"Expected status 200, got {login_response.status_code}"

    # Verifica se o token de acesso foi retornado com sucesso
    json_response = login_response.json()
    assert "access_token" in json_response, "Access token not found in response"
    assert (
        json_response["token_type"] == "bearer"
    ), f"Expected token type 'bearer', got {json_response['token_type']}"


# Teste de erro - senha incorreta
def test_login_invalid_password():
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert register_response.status_code == 200

    # Tenta fazer login com uma senha incorreta
    login_data = {
        "username": email,
        "password": "senha_errada",
    }
    login_response = login_user(login_data)
    assert (
        login_response.status_code == 401
    ), f"Expected status 401, got {login_response.status_code}"
    json_response = login_response.json()
    assert "detail" in json_response
    assert json_response["detail"] == "Incorrect email or password"


# Teste de erro - usuário não registrado
def test_login_unregistered_user():
    login_data = {
        "username": generate_random_email(),  # Gera um e-mail aleatório para garantir que não está registrado
        "password": "senha123",
    }
    login_response = login_user(login_data)
    assert (
        login_response.status_code == 401
    ), f"Expected status 401, got {login_response.status_code}"
    json_response = login_response.json()
    assert "detail" in json_response
    assert json_response["detail"] == "Incorrect email or password"


# Teste de erro - dados faltando (sem senha)
def test_login_missing_password():
    email = generate_random_email()
    register_data = {
        "name": "Test User",
        "email": email,
        "password": "senha123",
    }
    register_response = register_user(register_data)
    assert register_response.status_code == 200

    # Tenta fazer login sem senha
    login_data = {
        "username": email,
    }
    login_response = login_user(login_data)
    assert (
        login_response.status_code == 422
    ), f"Expected status 422, got {login_response.status_code}"
    json_response = login_response.json()
    assert "detail" in json_response
    assert json_response["detail"][0]["msg"] == "Field required"
    assert json_response["detail"][0]["loc"] == ["body", "password"]


# Tests de métodos não permitidos
@pytest.mark.parametrize("method", ["get", "put", "delete", "patch"])
def test_register_disallowed_methods(method):
    response = getattr(requests, method)(f"{BASE_URL}/user/login")
    assert (
        response.status_code == 405
    ), f"Expected 405 for {method.upper()}, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]
