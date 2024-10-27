import requests
import uuid
from tests.utils.test_utils import BASE_URL, register_user, generate_random_email

# Testes com o endpoint de registro de usuário

# Teste de erro - e-mail inválido
def test_register_invalid_email_format():
    data = {
        "name": "Matheus Fonseca",
        "email": "matheusfonsecaafonso",  # E-mail sem o domínio
        "password": "senha123",
    }
    response = register_user(data)
    assert (
        response.status_code == 400
    )  # Verifica se o status é 400 para erro de validação
    json_response = response.json()
    assert "detail" in json_response  # Verifica o campo "detail"
    assert (
        "The email must be in the format 'name@domain.com' or 'name@domain.br'." in json_response["detail"]
    )  # Verifica a mensagem correta


# Teste para e-mail sem domínio
def test_register_email_without_domain():
    data = {
        "name": "Matheus Fonseca",
        "email": "matheus@fonseca",  # E-mail sem domínio válido
        "password": "senha123",
    }
    response = register_user(data)
    assert (
        response.status_code == 400
    )  # Verifica se o status é 400 para erro de validação
    json_response = response.json()
    assert "detail" in json_response  # Verifica o campo "detail"
    assert (
        "The email must be in the format 'name@domain.com' or 'name@domain.br" in json_response["detail"]
    )  # Verifica a mensagem correta


# Teste para e-mail com domínio inválido
def test_register_email_invalid_domain():
    data = {
        "name": "Matheus Fonseca",
        "email": "matheus@domain.fake",  # Domínio não reconhecido
        "password": "senha123",
    }
    response = register_user(data)
    assert (
        response.status_code == 400
    )  # Verifica se o status é 400 para erro de validação
    json_response = response.json()
    assert "detail" in json_response  # Verifica o campo "detail"
    assert (
        "The email must be in the format 'name@domain.com' or 'name@domain.br'" in json_response["detail"]
    )  # Verifica a mensagem correta


# Teste de erro - e-mail duplicado
def test_register_duplicate_email():
    # Gerar um e-mail aleatório para evitar conflito
    random_email = generate_random_email()

    # Primeiro registro com um e-mail que será duplicado
    data = {
        "name": "Matheus Fonseca",
        "email": random_email,
        "password": "senha123",
    }
    response = register_user(data)
    assert response.status_code == 200  # Verifica se o primeiro registro é bem-sucedido

    # Tentativa de registro com o mesmo e-mail
    response = register_user(data)
    assert (
        response.status_code == 500
    )  # Ajustado para 400 se a API retornar isso em vez de 409
    json_response = response.json()
    assert "detail" in json_response
    assert (
        "already exists" in json_response["detail"]
    )  # Verifica parte da mensagem retornada

# Teste de erro - senha fraca
def test_register_weak_password():
    data = {
        "name": "Matheus Fonseca",
        "email": "matheusfonsecaafonso@gmail.com",
        "password": "123",  # Senha muito curta
    }
    response = register_user(data)
    assert (
        response.status_code == 400
    ), f"Expected status 400, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response  # Verifica o campo "detail"
    assert "The password must be at least 6 characters long." in json_response["detail"]

# Teste de sucesso - registro válido
def test_register_success():
    # Geração de nome e email aleatórios para garantir que o registro seja único
    unique_id = str(uuid.uuid4())[:8]  # Gera um identificador único curto
    data = {
        "name": f"Matheus Fonseca {unique_id}",
        "email": f"test_user_{unique_id}@gmail.com",
        "password": "senha123",
    }
    response = register_user(data)
    assert (
        response.status_code == 200
    ), f"Expected status 200, got {response.status_code}"
    json_response = response.json()
    assert "message" in json_response, "Key 'message' not found in response"
    assert (
        "successfully" in json_response["message"]
    ), f"Expected 'successfully!' in message, got {json_response['message']}"

# Teste de erro - dados faltando (sem nome)
def test_register_missing_name():
    data = {"email": "matheusfonsecaafonso@gmail.com", "password": "senha123"}
    response = register_user(data)
    assert response.status_code == 422  # Status code esperado para dados faltando
    json_response = response.json()
    assert "detail" in json_response
    assert json_response["detail"][0]["msg"] == "Field required"
    assert json_response["detail"][0]["loc"] == ["body", "name"]

# Teste de erro - método HTTP incorreto (GET)
def test_register_wrong_method_get():
    response = requests.get(f"{BASE_URL}/user/register")
    assert response.status_code == 405
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]

# Teste de erro - método HTTP incorreto (PUT)
def test_register_wrong_method_put():
    response = requests.put(f"{BASE_URL}/user/register")
    assert response.status_code == 405
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]

# Teste de erro - método HTTP incorreto (PATCH)
def test_register_wrong_method_patch():
    response = requests.patch(f"{BASE_URL}/user/register")
    assert response.status_code == 405
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]

# Teste de erro - método HTTP incorreto (DELETE)
def test_register_wrong_method_delete():
    response = requests.delete(f"{BASE_URL}/user/register")
    assert response.status_code == 405
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]
