from typing import Dict
from src.fintrack_api.models.userModels import UserIn
from src.fintrack_api.services.CRUD import create_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, Depends, status
from src.fintrack_api.dependencies import authenticate_user, create_access_token
from src.fintrack_api.utils.frintrack_api_utils import (
    validate_email_format,
    validate_password_strength,
)

# -------------------- USER ROUTES -------------------- #

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.post("/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Dict[str, str]:
    """
    Authenticate a user and generate an access token.

    Args:
        form_data (OAuth2PasswordRequestForm): Form data containing the user's
        email and password for authentication.

    Returns:
        Dict[str, str]: A dictionary with the access token and its type.

    Raises:
        HTTPException: If authentication fails due to incorrect credentials.
    """
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.post("/register", response_model=Dict[str, str])
async def register_new_user(user: UserIn) -> Dict[str, str]:
    """
    Register a new user in the system.

    Args:
        user (UserIn): The user data provided for registration.

    Returns:
        Dict[str, str]: A message confirming the successful registration.

    Raises:
        HTTPException: If email validation, password validation, or user creation fails.
    """
    try:
        validate_email_format(user.email)

        validate_password_strength(user.password)

        await create_user(user)
        return {"message": f"User {user.name} registered successfully!"}
    except ValueError as val_exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(val_exc)
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error registering user: {str(exc)}",
        )