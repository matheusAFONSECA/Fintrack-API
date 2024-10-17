from datetime import timedelta
from typing import Annotated, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fintrack_api.dependencies import (
    authenticate_user,
    create_access_token,
    get_api_key,
    get_password_hash,
)
from fintrack_api.services.user import create_user
from fintrack_api.models.userModels import UserInDB, UserIn
from fintrack_api.models.structural.TokenModels import Token


class API:
    """
    Classe API que encapsula todas as rotas e funcionalidades da aplicação.
    """

    def __init__(self):
        """
        Inicializa o roteador com prefixo e dependências.
        """
        self.router = APIRouter(
            prefix="/user",
            tags=["User"],
            dependencies=[Depends(get_api_key)],
        )
        self.setup_routes()

    def setup_routes(self):
        """
        Define as rotas da API.
        """
        self.router.post("/login", response_model=Token)(self.login_for_access_token)
        self.router.post("/register", response_model=Dict)(self.register_new_user)

    async def login_for_access_token(
        self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ) -> Token:
        """
        Autentica o usuário e retorna um token de acesso JWT.

        Args:
            form_data (OAuth2PasswordRequestForm): Dados de login (email e senha).

        Returns:
            Token: Token JWT válido para autenticação.

        Raises:
            HTTPException: Se o login falhar por email ou senha incorretos.
        """
        user: UserInDB = await authenticate_user(form_data.username, form_data.password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Define o tempo de expiração do token
        access_token_expires = timedelta(minutes=30)  # 30 minutos de validade
        access_token = create_access_token(
            data={"sub": user.user_id}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")

    async def register_new_user(self, user: UserIn) -> Dict:
        """
        Registra um novo usuário no sistema.

        Args:
            user (UserIn): Dados do novo usuário.

        Returns:
            Dict: Mensagem indicando sucesso no registro.

        Raises:
            HTTPException: Se ocorrer um erro durante o registro.
        """
        try:
            # Gerar o hash da senha corretamente a partir do objeto user
            hashed_password = get_password_hash(user.password)
            
            # Substituir a senha em texto pelo hash
            user.password = hashed_password

            # Criar o usuário usando a função create_user
            await create_user(user)

            return {"message": f"Usuário {user.name} registrado com sucesso!"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao registrar usuário: {str(e)}"
            )