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
    def __init__(self):
        """
        Inicializa o roteador com prefixo e dependências.
        """
        self.router = APIRouter(
            prefix="/user",
            tags=["User"],
        )
        self.setup_routes()

    def setup_routes(self):
        """
        Define as rotas da API.
        """
        # A rota de login e registro não deve ter dependência de autenticação
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

    # Função para verificar a força da senha
    def validate_password_strength(self, password: str):
        if len(password) < 6:
            raise HTTPException(
                status_code=400,  # Retorna 400 para erro de validação
                detail="A senha deve ter no mínimo 6 caracteres."
            )

    async def register_new_user(self, user: UserIn) -> Dict:
        """
        Registra um novo usuário no sistema.
        """
        try:
            # Validação da força da senha antes de qualquer operação
            self.validate_password_strength(user.password)

            # Gerar o hash da senha corretamente a partir do objeto user
            hashed_password = get_password_hash(user.password)
            
            # Substituir a senha em texto pelo hash
            user.password = hashed_password

            # Criar o usuário usando a função create_user
            await create_user(user)

            return {"message": f"Usuário {user.name} registrado com sucesso!"}
        
        except HTTPException as http_exc:
            raise http_exc  # Relevanta o HTTPException existente
        except Exception as e:
            # Lança um erro 400 para problemas genéricos no registro
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao registrar usuário: {str(e)}"
            )
