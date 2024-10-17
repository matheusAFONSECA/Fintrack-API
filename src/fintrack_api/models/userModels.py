from typing import Optional
from pydantic import BaseModel, Field


class UserOut(BaseModel):
    """
    Modelo de saída para exibir os dados de um usuário.

    Attributes:
        name (str): Nome do usuário.
        email (str): Email do usuário.
    """

    name: str = Field(max_length=150)
    email: str = Field(max_length=100)


class UserIn(UserOut):
    """
    Modelo para representar os dados de entrada ao registrar um usuário.

    Attributes:
        password (str): Senha do usuário.
    """

    password: str = Field(max_length=64)


class UserInDB(BaseModel):
    """
    Modelo para representar um usuário armazenado no banco de dados.

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
