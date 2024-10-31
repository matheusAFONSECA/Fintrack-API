from typing import Dict
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fintrack_api.models.userModels import UserIn
from fintrack_api.services.CRUD import create_user
from fintrack_api.dependencies import authenticate_user, create_access_token
from fintrack_api.services.CRUD.create import AddItem, add_item_to_db
from fintrack_api.services.CRUD.read import get_all_items_from_db
from fintrack_api.utils.frintrack_api_utils import (
    validate_email_format,
    validate_password_strength,
)

router = APIRouter()

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


@router.post("/user/register", response_model=Dict[str, str])
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


# -------------------- ADD ROUTES -------------------- #

add_router = APIRouter(prefix="/add", tags=["Add"])


@add_router.post("/revenue")
async def add_revenue(item: AddItem):
    """
    Add a revenue entry to the database.

    Args:
        item (AddItem): Data representing the revenue to be added.

    Returns:
        Dict[str, str]: A message confirming the successful addition.
    """
    return await add_item_to_db("revenue", item)


@add_router.post("/expenditure")
async def add_expenditure(item: AddItem):
    """
    Add an expenditure entry to the database.

    Args:
        item (AddItem): Data representing the expenditure to be added.

    Returns:
        Dict[str, str]: A message confirming the successful addition.
    """
    return await add_item_to_db("expenditure", item)


@add_router.post("/alert")
async def add_alert(item: AddItem):
    """
    Add an alert entry to the database.

    Args:
        item (AddItem): Data representing the alert to be added.

    Returns:
        Dict[str, str]: A message confirming the successful addition.
    """
    return await add_item_to_db("alert", item)


@add_router.post("/reminder")
async def add_reminder(item: AddItem):
    """
    Add a reminder entry to the database.

    Args:
        item (AddItem): Data representing the reminder to be added.

    Returns:
        Dict[str, str]: A message confirming the successful addition.
    """
    return await add_item_to_db("reminder", item)


# -------------------- VISUALIZATION ROUTES -------------------- #

visualization_router = APIRouter(prefix="/visualization", tags=["Visualization"])


@visualization_router.get("/revenue")
async def get_all_revenue():
    """
    Retrieve all revenue entries from the database.

    Returns:
        List[Dict]: A list of all revenue entries.
    """
    return await get_all_items_from_db("revenue")


@visualization_router.get("/expenditure")
async def get_all_expenditure():
    """
    Retrieve all expenditure entries from the database.

    Returns:
        List[Dict]: A list of all expenditure entries.
    """
    return await get_all_items_from_db("expenditure")


@visualization_router.get("/alert")
async def get_all_alerts():
    """
    Retrieve all alert entries from the database.

    Returns:
        List[Dict]: A list of all alert entries.
    """
    return await get_all_items_from_db("alert")


@visualization_router.get("/reminder")
async def get_all_reminders():
    """
    Retrieve all reminder entries from the database.

    Returns:
        List[Dict]: A list of all reminder entries.
    """
    return await get_all_items_from_db("reminder")


# -------------------- INCLUDE ROUTERS -------------------- #

router.include_router(user_router)
router.include_router(add_router)
router.include_router(visualization_router)
