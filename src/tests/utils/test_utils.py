import random
import string
import requests

# URL base da API
BASE_URL = "https://fintrack-api.vercel.app"


# Função auxiliar para registro de usuário
def register_user(data):
    return requests.post(f"{BASE_URL}/user/register", json=data)


# Função auxiliar para login do usuário
def login_user(data):
    return requests.post(f"{BASE_URL}/user/login", data=data)

# Função auxliar para adicionar um novo alerta
def add_alert(data):
    return requests.post(f"{BASE_URL}/add/alert", json=data)

def add_reminder(data):
    return requests.post(f"{BASE_URL}/add/reminder", json=data)


# Função auxiliar para gerar um e-mail aleatório
def generate_random_email():
    random_str = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{random_str}@gmail.com"

# Função auxiliar para gerar uma data aleatória
def generate_random_date():
    random_day = random.randint(1, 28)
    random_month = random.randint(1, 12)
    random_year = random.randint(1900, 2021)
    return f"{random_year}-{random_month}-{random_day}"
