import re
from fastapi import HTTPException

# Função para verificar a força da senha
def validate_password_strength(password: str):
    if len(password) < 6:
        raise HTTPException(
            status_code=400,  # Retorna 400 para erro de validação
            detail="A senha deve ter no mínimo 6 caracteres."
        )
    
# Função para validar o formato do e-mail
def validate_email_format(email: str) -> None:
    pattern = r'^[\w\.-]+@[\w\.-]+\.(com|br)$'
    if not re.match(pattern, email):
        raise ValueError("O e-mail deve estar no formato 'nome@dominio.com' ou 'nome@dominio.br'.")
