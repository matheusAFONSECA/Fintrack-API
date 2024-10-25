import re
from fastapi import HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Gera um hash para uma senha."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha corresponde ao hash."""
    return pwd_context.verify(plain_password, hashed_password)


# Função para verificar a força da senha
def validate_password_strength(password: str):
    if len(password) < 6:
        raise HTTPException(
            status_code=400,  # Retorna 400 para erro de validação
            detail="A senha deve ter no mínimo 6 caracteres.",
        )


# Função para validar o formato do e-mail
def validate_email_format(email: str) -> None:
    pattern = r"^[\w\.-]+@[\w\.-]+\.(com|br)$"
    if not re.match(pattern, email):
        raise ValueError(
            "O e-mail deve estar no formato 'nome@dominio.com' ou 'nome@dominio.br'."
        )
