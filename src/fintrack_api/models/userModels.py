from typing import Optional
from pydantic import BaseModel, Field


class UserOut(BaseModel):
    """
    Modelo para representar a saída de dados de um usuário.

    Attributes:
        name (str): Nome do usuário (máximo de 150 caracteres).
        email (str): Email do usuário (máximo de 100 caracteres).
        phone (str): Telefone do usuário (máximo de 15 caracteres).
        birth (str): Data de nascimento do usuário no formato 'DD/MM/AAAA'.
    """

    name: str = Field(max_length=150)
    email: str = Field(max_length=100)
    phone: str = Field(max_length=15)
    birth: str = Field(max_length=10)


class UserIn(UserOut):
    """
    Modelo para representar os dados de entrada ao criar um novo usuário.

    Attributes:
        cpf (str): CPF do usuário (máximo de 14 caracteres).
        password (str): Senha do usuário (máximo de 64 caracteres).
    """

    cpf: str = Field(max_length=14)
    password: str = Field(max_length=64)


class UserInDB(BaseModel):
    """
    Modelo para representar o usuário armazenado no banco de dados.

    Attributes:
        hashed_password (str): Hash da senha do usuário.
        user_id (str): Identificador único do usuário.
    """

    hashed_password: str
    user_id: str


class UserInQuery(BaseModel):
    """
    Modelo para representar consultas baseadas em dados opcionais do usuário.

    Attributes:
        name (Optional[str]): Nome do usuário (máximo de 150 caracteres).
        email (Optional[str]): Email do usuário (máximo de 100 caracteres).
        phone (Optional[str]): Telefone do usuário (máximo de 15 caracteres).
        birth (Optional[str]): Data de nascimento do usuário no formato 'DD/MM/AAAA'.
    """

    name: Optional[str] = Field(None, max_length=150)
    email: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=15)
    birth: Optional[str] = Field(None, max_length=10)
