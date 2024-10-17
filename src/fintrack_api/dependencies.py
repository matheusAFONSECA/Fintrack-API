import os
import jwt
from dotenv import load_dotenv
from typing import Annotated, Union
from fintrack_api.models.userModels import UserInDB
from passlib.context import CryptContext
from jwt import InvalidTokenError
# from jwt.exceptions import InvalidTokenError
from starlette.status import HTTP_403_FORBIDDEN
from fintrack_api.services.user import get_user_by_email_for_auth
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from fintrack_api.models.structural.TokenModels import TokenData

# Carrega variáveis de ambiente
load_dotenv()

# Configuração de cabeçalho de autenticação por API key
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# Variáveis secretas para JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Contexto de criptografia para senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de autenticação OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_api_key(X_API_Key: str = Security(api_key_header)) -> str:
    """
    Valida a API key fornecida no cabeçalho da solicitação.

    Args:
        X_API_Key (str): A API key recebida do cabeçalho.

    Returns:
        str: A API key válida.

    Raises:
        HTTPException: Se a API key for inválida ou não fornecida.
    """
    if X_API_Key == os.getenv("API_KEY"):
        return X_API_Key
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN, 
        detail="Could not validate API KEY"
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha fornecida corresponde ao hash armazenado.

    Args:
        plain_password (str): A senha em texto plano.
        hashed_password (str): O hash da senha armazenado.

    Returns:
        bool: True se a senha for válida, caso contrário, False.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Gera um hash para uma senha.

    Args:
        password (str): A senha em texto plano.

    Returns:
        str: O hash da senha.
    """
    return pwd_context.hash(password)


async def authenticate_user(email: str, password: str) -> Union[UserInDB, bool]:
    """
    Autentica o usuário com base no email e senha fornecidos.

    Args:
        email (str): O email do usuário.
        password (str): A senha em texto plano do usuário.

    Returns:
        Union[UserInDB, bool]: O objeto UserInDB se a autenticação for bem-sucedida, 
        caso contrário, False.
    """
    user: UserInDB = await get_user_by_email_for_auth(email)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    """
    Cria um token de acesso JWT.

    Args:
        data (dict): Os dados a serem codificados no token.
        expires_delta (Union[timedelta, None], opcional): A duração do token.

    Returns:
        str: O token JWT codificado.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=999))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    """
    Obtém o usuário atual com base no token JWT fornecido.

    Args:
        token (str): O token JWT fornecido na solicitação.

    Returns:
        UserInDB: O objeto do usuário autenticado.

    Raises:
        HTTPException: Se o token for inválido ou se o usuário não existir.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except InvalidTokenError:
        raise credentials_exception

    user = await get_user_by_email_for_auth(token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_user_id(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    """
    Obtém o ID do usuário atual com base no token JWT fornecido.

    Args:
        token (str): O token JWT fornecido na solicitação.

    Returns:
        str: O ID do usuário.

    Raises:
        Exception: Se o token for inválido.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        return user_id
    except InvalidTokenError:
        raise Exception("Invalid token")
