from typing import Dict
from src.fintrack_api.models.userModels import UserIn
from src.fintrack_api.services.user import create_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from src.fintrack_api.dependencies import authenticate_user, create_access_token
from src.fintrack_api.utils.frintrack_api_utils import validate_email_format, validate_password_strength

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Dict[str, str]:
    """
    Authenticate a user and generate an access token.

    Args:
        form_data (OAuth2PasswordRequestForm): The login form containing
        the user's email and password.

    Returns:
        dict: A dictionary with the access token and token type.

    Raises:
        HTTPException: If authentication fails due to incorrect credentials.
    """
    print(
        f"Login request: username={form_data.username}, password={form_data.password}"
    )  # Debug

    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        print("Authentication failed.")  # Debug
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    print(f"Generated token: {access_token}")  # Debug

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=Dict[str, str])
async def register_new_user(user: UserIn) -> Dict[str, str]:
    """
    Register a new user in the system.

    Args:
        user (UserIn): The user data provided for registration.

    Returns:
        dict: A message confirming successful registration.

    Raises:
        HTTPException: If an error occurs during user creation.
    """
    try:
        # Validação do formato do e-mail
        validate_email_format(user.email)

        # Validação da força da senha antes de qualquer operação
        validate_password_strength(user.password)

        await create_user(user)

        return {"message": f"User {user.name} registered successfully!"}
    except HTTPException as http_exc:
        raise http_exc  # Relevanta o HTTPException existente
    except ValueError as val_exc:
        # Lança um erro 400 para problemas de validação do e-mail
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(val_exc)
        )
    except Exception as e:
        # Lança um erro 400 para problemas genéricos no registro
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao registrar usuário: {str(e)}"
        )
    
