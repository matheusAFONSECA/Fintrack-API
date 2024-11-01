from typing import Dict, Optional
from fintrack_api.models.userModels import UserIn
from fintrack_api.services.CRUD import create_user
from fastapi.security import OAuth2PasswordRequestForm
from fintrack_api.services.CRUD.read import get_all_items_from_db
from fastapi import APIRouter, HTTPException, Depends, Query, status
from fintrack_api.services.CRUD.create import AddItem, add_item_to_db
from fintrack_api.dependencies import authenticate_user, create_access_token
from fintrack_api.utils.frintrack_api_utils import (
    validate_email_format,
    validate_password_strength,
)
from fintrack_api.services.CRUD.update import (
    update_revenue_by_email,
    update_expenditure_by_email,
    update_alert_by_email,
    update_reminder_by_email,
)
from fintrack_api.services.CRUD.delete import (
    delete_revenue_by_email,
    delete_expenditure_by_email,
    delete_alert_by_email,
    delete_reminder_by_email,
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
async def get_all_revenue(email: Optional[str] = Query(None)):
    """
    Retrieve all revenue entries, optionally filtered by email.

    Args:
        email (Optional[str]): The email to filter the results by (if provided).

    Returns:
        List[Dict[str, str]]: A list of revenue entries.
    """
    return await get_all_items_from_db("revenue", email)


@visualization_router.get("/expenditure")
async def get_all_expenditure(email: Optional[str] = Query(None)):
    """
    Retrieve all expenditure entries, optionally filtered by email.

    Args:
        email (Optional[str]): The email to filter the results by (if provided).

    Returns:
        List[Dict[str, str]]: A list of expenditure entries.
    """
    return await get_all_items_from_db("expenditure", email)


@visualization_router.get("/alert")
async def get_all_alerts(email: Optional[str] = Query(None)):
    """
    Retrieve all alert entries, optionally filtered by email.

    Args:
        email (Optional[str]): The email to filter the results by (if provided).

    Returns:
        List[Dict[str, str]]: A list of alert entries.
    """
    return await get_all_items_from_db("alert", email)


@visualization_router.get("/reminder")
async def get_all_reminders(email: Optional[str] = Query(None)):
    """
    Retrieve all reminder entries, optionally filtered by email.

    Args:
        email (Optional[str]): The email to filter the results by (if provided).

    Returns:
        List[Dict[str, str]]: A list of reminder entries.
    """
    return await get_all_items_from_db("reminder", email)


# -------------------- UPDATE ROUTES -------------------- #

update_router = APIRouter(prefix="/update", tags=["Update"])


@update_router.put("/revenue")
async def update_revenue(email: str, updated_data: dict):
    """Update a revenue entry by email."""
    return await update_revenue_by_email(email, updated_data)


@update_router.put("/expenditure")
async def update_expenditure(email: str, updated_data: dict):
    """Update an expenditure entry by email."""
    return await update_expenditure_by_email(email, updated_data)


@update_router.put("/alert")
async def update_alert(email: str, updated_data: dict):
    """Update an alert entry by email."""
    return await update_alert_by_email(email, updated_data)


@update_router.put("/reminder")
async def update_reminder(email: str, updated_data: dict):
    """Update a reminder entry by email."""
    return await update_reminder_by_email(email, updated_data)


# -------------------- DELETE ROUTES -------------------- #

delete_router = APIRouter(prefix="/delete", tags=["Delete"])


@delete_router.delete("/revenue")
async def delete_revenue(email: str):
    """Delete a revenue entry by email."""
    return await delete_revenue_by_email(email)


@delete_router.delete("/expenditure")
async def delete_expenditure(email: str):
    """Delete an expenditure entry by email."""
    return await delete_expenditure_by_email(email)


@delete_router.delete("/alert")
async def delete_alert(email: str):
    """Delete an alert entry by email."""
    return await delete_alert_by_email(email)


@delete_router.delete("/reminder")
async def delete_reminder(email: str):
    """Delete a reminder entry by email."""
    return await delete_reminder_by_email(email)


# -------------------- INCLUDE ROUTERS -------------------- #

router.include_router(update_router)
router.include_router(delete_router)
router.include_router(user_router)
router.include_router(add_router)
router.include_router(visualization_router)
