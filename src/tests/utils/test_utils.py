import random
import string
import requests

# URL base da API
BASE_URL = "http://localhost:8000"

# ---------------------- Funções de registro e login ----------------------


# Função auxiliar para registro de usuário
def register_user(data):
    return requests.post(f"{BASE_URL}/user/register", json=data)


# Função auxiliar para login do usuário
def login_user(data):
    return requests.post(f"{BASE_URL}/user/login", data=data)


# ---------------------- Funções de adição ----------------------


# Função auxliar para adicionar um novo alerta
def add_alert(data):
    return requests.post(f"{BASE_URL}/add/alert", json=data)


# Função auxiliar para adicionar um novo lembrete
def add_reminder(data):
    return requests.post(f"{BASE_URL}/add/reminder", json=data)


# Função auxiliar para adicionar uma nova receita
def add_revenue(data):
    return requests.post(f"{BASE_URL}/add/revenue", json=data)


# ---------------------- Funções de visualização ----------------------


# Função auxiliar para adicionar uma nova despesa
def add_expenditure(data):
    return requests.post(f"{BASE_URL}/add/expenditure", json=data)


# Função auxiliar para visualizar um alerta
def visualize_alert(data):
    return requests.get(f"{BASE_URL}/visualization/alert", params=data)


# Função auxiliar para visualizar uma receita
def visualize_revenue(data):
    return requests.get(f"{BASE_URL}/visualization/revenue", params=data)


# Função auxiliar para visualizar um lembrete
def visualize_reminder(data):
    return requests.get(f"{BASE_URL}/visualization/reminder", params=data)


# Função auxiliar para visualizar uma despesa
def visualize_expenditure(data):
    return requests.get(f"{BASE_URL}/visualization/expenditure", params=data)

# ---------------------- Funções de exclusão ----------------------

# Função auxiliar para deletar um alerta
def delete_alert(data):
    return requests.delete(f"{BASE_URL}/delete/alert", params=data)


# ---------------------- Funções auxiliares ----------------------


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
