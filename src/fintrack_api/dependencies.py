import os
import jwt
from dotenv import load_dotenv
from typing import Annotated, Optional, Union
from fintrack_api.models.userModels import UserInDB
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError
from fintrack_api.services.user import get_user_by_email_for_auth
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from fintrack_api.models.structural.TokenModels import TokenData
from passlib.context import CryptContext  # noqa: F811
from fintrack_api.utils.frintrack_api_utils import verify_password


# Inicialize o contexto de criptografia (caso ainda não tenha)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Carrega variáveis de ambiente
load_dotenv()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


# Variáveis secretas para JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Contexto de criptografia para senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de autenticação OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_api_key(X_API_Key: str = Security(api_key_header)) -> str:
    if X_API_Key == os.getenv("API_KEY"):
        return X_API_Key
    raise HTTPException(status_code=403, detail="Could not validate API KEY")


async def authenticate_user(email: str, password: str) -> Optional[UserInDB]:
    user = await get_user_by_email_for_auth(email)
    print(f"User from DB: {user}")  # Log para debug

    if not user:
        print("User not found.")
        return None

    if not verify_password(password, user.hashed_password):  # Verificação correta
        print("Password mismatch.")
        return None

    print("User authenticated successfully.")
    return user


def create_access_token(
    data: dict, expires_delta: Union[timedelta, None] = None
) -> str:
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
