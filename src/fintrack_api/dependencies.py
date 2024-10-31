import os
import jwt
from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError
from typing import Annotated, Optional, Union
from datetime import datetime, timedelta, timezone
from fintrack_api.models.userModels import UserInDB
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from fintrack_api.services.CRUD import get_user_by_email_for_auth
from fintrack_api.models.structural.TokenModels import TokenData

# Load environment variables
load_dotenv()

# Initialize authentication schemes
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Secret and algorithm for JWT
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


def create_access_token(
    data: dict, expires_delta: Union[timedelta, None] = None
) -> str:
    """
    Create a JWT access token with an optional expiration.

    Args:
        data (dict): The data to encode in the token.
        expires_delta (Union[timedelta, None]): Optional expiration time for the token.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=999))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_user(email: str, password: str) -> Optional[UserInDB]:
    """
    Authenticate a user with the provided email and password.

    Args:
        email (str): The user's email.
        password (str): The user's password.

    Returns:
        Optional[UserInDB]: The authenticated user if successful, otherwise None.
    """
    print(f"Attempting to authenticate: email={email}, password={password}")  # Debug

    user = await get_user_by_email_for_auth(email)
    if not user:
        print("User not found.")  # Debug
        return None

    print(f"User found: {user}")  # Debug

    if password != user.password:
        print(
            f"Incorrect password. Provided: {password}, Expected: {user.password}"
        )  # Debug
        return None

    print("User successfully authenticated.")  # Debug
    return user


async def get_api_key(X_API_Key: str = Security(api_key_header)) -> str:
    """
    Validate the provided API key.

    Args:
        X_API_Key (str): The API key provided in the request header.

    Returns:
        str: The valid API key.

    Raises:
        HTTPException: If the API key is invalid.
    """
    if X_API_Key == os.getenv("API_KEY"):
        return X_API_Key
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    """
    Retrieve the current user based on the provided JWT token.

    Args:
        token (str): The JWT token from the request.

    Returns:
        UserInDB: The authenticated user.

    Raises:
        HTTPException: If the token is invalid or user is not found.
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
    Retrieve the current user's ID from the provided JWT token.

    Args:
        token (str): The JWT token from the request.

    Returns:
        str: The user ID extracted from the token.

    Raises:
        Exception: If the token is invalid or contains no user ID.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise Exception("Invalid token payload")
        return user_id
    except InvalidTokenError:
        raise Exception("Invalid token")
