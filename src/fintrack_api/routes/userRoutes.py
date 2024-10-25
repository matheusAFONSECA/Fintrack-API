from datetime import timedelta
from typing import Annotated, Optional, List, Dict
from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fintrack_api.dependencies import (
    authenticate_user,
    create_access_token,
    get_api_key,
)
from services.user import create_user, get_all_users
from fintrack_api.models.userModels import UserInDB, UserOut, UserIn
from fintrack_api.models.structural.TokenModels import Token

# Definição do roteador com prefixo e dependências
router = APIRouter(prefix="/user", tags=["User"], dependencies=[Depends(get_api_key)])


@router.post("/login", response_model=Token)
async def login_for_access_token(
    email: Annotated[str, Form()],
    password: Annotated[str, Form()]
) -> Token:
    user: UserInDB = await authenticate_user(email, password)

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token_expires = timedelta(days=999)
    access_token = create_access_token(
        data={"sub": user.user_id},  # Agora o sub é o email do usuário
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")



@router.post("/register", response_model=Dict)
async def register_new_user(user: UserIn) -> Dict:
    """
    Registra um novo usuário no sistema.

    Args:
        user (UserIn): Dados do usuário a serem registrados.

    Returns:
        Dict: Mensagem indicando sucesso no registro.

    Raises:
        Exception: Se ocorrer um erro durante o registro do usuário.
    """
    try:
        await create_user(user)
        return {"message": f"User with name {user.name} created successfully!"}
    except Exception as e:
        raise e


@router.get("/", response_model=Optional[List[UserOut]])
async def get_all() -> Optional[List[UserOut]]:
    """
    Recupera todos os usuários registrados no sistema.

    Returns:
        Optional[List[UserOut]]: Lista de usuários registrados ou None, se não houver.

    Raises:
        Exception: Se ocorrer um erro ao recuperar os usuários.
    """
    try:
        users = await get_all_users()
        return users
    except Exception as e:
        raise e
