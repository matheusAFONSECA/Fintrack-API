import requests
import pytest

# URL base da API
BASE_URL = "http://localhost:8000"

# Função auxiliar para registro de usuário
def register_user(data):
    return requests.post(f"{BASE_URL}/user/register", json=data)

# Teste de sucesso - registro válido
def test_register_success():
    data = {
        "name": "Matheus Fonseca",
        "email": "maa@gmail.com",
        "password": "senha"
    }
    response = register_user(data)
    assert response.status_code == 201
    json_response = response.json()
    assert "message" in json_response
    assert "sucesso" in json_response["message"]

# Teste de erro - e-mail duplicado
def test_register_duplicate_email():
    data = {
        "name": "Matheus Fonseca",
        "email": "matheusfonsecaafonso@gmail.com",  # Mesmo e-mail usado no teste anterior
        "password": "senha"
    }
    response = register_user(data)
    assert response.status_code == 409
    json_response = response.json()
    assert "message" in json_response
    assert "E-mail já registrado" in json_response["message"]

# Teste de erro - dados faltando (sem nome)
def test_register_missing_name():
    data = {
        "email": "matheusfonsecaafonso@gmail.com",
        "password": "senha"
    }
    response = register_user(data)
    assert response.status_code == 400
    json_response = response.json()
    assert "message" in json_response
    assert "O campo nome é obrigatório" in json_response["message"]

# Teste de erro - e-mail inválido
def test_register_invalid_email():
    data = {
        "name": "Matheus Fonseca",
        "email": "matheusfonsecaafonso",  # E-mail inválido
        "password": "senha"
    }
    response = register_user(data)
    assert response.status_code == 400
    json_response = response.json()
    assert "message" in json_response
    assert "Formato de e-mail inválido" in json_response["message"]

# Teste de erro - senha fraca
def test_register_weak_password():
    data = {
        "name": "Matheus Fonseca",
        "email": "matheusfonsecaafonso@gmail.com",
        "password": "123"  # Senha muito curta
    }
    response = register_user(data)
    assert response.status_code == 400
    json_response = response.json()
    assert "message" in json_response
    assert "A senha deve ter no mínimo 6 caracteres" in json_response["message"]

# Teste de erro - método HTTP incorreto
def test_register_wrong_method():
    response = requests.get(f"{BASE_URL}/user/register")
    assert response.status_code == 405
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]

