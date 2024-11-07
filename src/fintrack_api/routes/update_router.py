from fastapi import APIRouter, HTTPException
from fintrack_api.services.CRUD.read import get_all_items_from_db
from fintrack_api.services.CRUD.update import (
    update_revenue_by_email,
    update_expenditure_by_email,
    update_alert_by_email,
    update_reminder_by_email,
)
from fintrack_api.utils.frintrack_api_utils import validate_email_format

# -------------------- UPDATE ROUTES -------------------- #

update_router = APIRouter(prefix="/update", tags=["Update"])

EMAIL_REQUIRED = "The 'email' parameter is required."
EMAIL_NOT_FOUND = "Email not found"


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
    """
    Updates an alert entry by email.

    Parameters:
        email (str): The email associated with the alert to update.
        updated_data (dict): A dictionary containing the updated data fields for the alert.

    Raises:
        HTTPException: If the email is not provided, has an invalid format, or does not exist in the database.

    Returns:
        dict: A dictionary with a success message upon successful update.
    """
    # Check if the email parameter is provided
    if email is None:
        raise HTTPException(status_code=400, detail=EMAIL_REQUIRED)

    # Validate the email format and check if there are matching entries in the database
    if email:
        validate_email_format(email)

        # Query the database using the provided email
        alerts = await get_all_items_from_db("alert", email)
        if not alerts:
            raise HTTPException(status_code=404, detail=EMAIL_NOT_FOUND)

        # Update the alert entry
        response = await update_alert_by_email(email, updated_data)

    return {"message": response}


@update_router.put("/reminder")
async def update_reminder(email: str, updated_data: dict):
    """Update a reminder entry by email."""
    return await update_reminder_by_email(email, updated_data)
