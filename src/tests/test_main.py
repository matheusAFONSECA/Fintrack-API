import requests

# URL base da API
BASE_URL = "http://localhost:8000"

# Função auxiliar para registro de usuário
def register_user(data):
    return requests.post(f"{BASE_URL}/user/register", json=data)

# Teste de erro - dados faltando (sem nome)
def test_register_missing_name():
    data = {
        "email": "matheusfonsecaafonso@gmail.com",
        "password": "senha123"
    }
    response = register_user(data)
    assert response.status_code == 422  # Status code esperado para dados faltando
    json_response = response.json()
    assert "detail" in json_response
    assert json_response["detail"][0]["msg"] == "Field required"
    assert json_response["detail"][0]["loc"] == ["body", "name"]

# Teste de erro - senha fraca
def test_register_weak_password():
    data = {
        "name": "Matheus Fonseca",
        "email": "matheusfonsecaafonso@gmail.com",
        "password": "123"  # Senha muito curta
    }
    response = register_user(data)
    assert response.status_code == 400, f"Expected status 400, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response  # Verifica o campo "detail"
    assert "A senha deve ter no mínimo 6 caracteres" in json_response["detail"]

# Teste de erro - método HTTP incorreto
def test_register_wrong_method():
    response = requests.get(f"{BASE_URL}/user/register")
    assert response.status_code == 405
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]
