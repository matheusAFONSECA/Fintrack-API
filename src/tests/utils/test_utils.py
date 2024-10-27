import random
import string
import requests
import bcrypt

# URL base da API
BASE_URL = "http://localhost:8000"


# Função auxiliar para registro de usuário
def register_user(data):
    return requests.post(f"{BASE_URL}/user/register", json=data)


# Função auxiliar para login do usuário
def login_user(data):
    return requests.post(f"{BASE_URL}/user/login", data=data)


# Função auxiliar para gerar um e-mail aleatório
def generate_random_email():
    random_str = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{random_str}@gmail.com"

# Função auxiliar para hash de senha
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
