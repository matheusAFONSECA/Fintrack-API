import random
import string
import requests

# URL base da API
BASE_URL = "http://localhost:8000"

# Função auxiliar para registro de usuário
def register_user(data):
    return requests.post(f"{BASE_URL}/user/register", json=data)

# Função auxiliar para gerar um e-mail aleatório
def generate_random_email():
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{random_str}@gmail.com"