from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Body
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
async def update_revenue(
    email: Optional[str] = Query(None), updated_data: Optional[dict] = Body(None)
):
    """
    Updates a revenue entry by email.

    Parameters:
        email (str): The email associated with the revenue to update.
        updated_data (dict): A dictionary containing the updated data fields for the revenue.

    Raises:
        HTTPException: If the email is not provided, has an invalid format, or does not exist in the database.

    Returns:
        dict: A dictionary with a success message upon successful update.
    """
    # Check if the email parameter is provided
    if email is None:
        raise HTTPException(
            status_code=400, detail="The 'email' parameter is required."
        )

    # Validate the email format
    validate_email_format(email)

    # Query the database using the provided email
    revenues = await get_all_items_from_db("revenue", email)
    if not revenues:
        raise HTTPException(status_code=404, detail="Email not found.")

    # Update the revenue entry
    response = await update_revenue_by_email(email, updated_data)
    return response


@update_router.put("/expenditure")
async def update_expenditure(
    email: Optional[str] = Query(None), updated_data: Optional[dict] = Body(None)
):
    """
    Updates an expenditure entry by email.

    Parameters:
        email (str): The email associated with the expenditure to update.
        updated_data (dict): A dictionary containing the updated data fields for the expenditure.

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
        expenditures = await get_all_items_from_db("expenditure", email)
        if not expenditures:
            raise HTTPException(status_code=404, detail=EMAIL_NOT_FOUND)

        # Update the expenditure entry
        response = await update_expenditure_by_email(email, updated_data)

    return response


@update_router.put("/alert")
async def update_alert(
    email: Optional[str] = Query(None), updated_data: Optional[dict] = Body(None)
):
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

    return response


@update_router.put("/reminder")
async def update_reminder(
    email: Optional[str] = Query(None), updated_data: Optional[dict] = Body(None)
):
    """
    Updates a reminder entry by email.

    Parameters:
        email (str): The email associated with the reminder to update.
        updated_data (dict): A dictionary containing the updated data fields for the reminder.

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
        reminders = await get_all_items_from_db("reminder", email)
        if not reminders:
            raise HTTPException(status_code=404, detail=EMAIL_NOT_FOUND)

        # Update the reminder entry
        response = await update_reminder_by_email(email, updated_data)

    return response
