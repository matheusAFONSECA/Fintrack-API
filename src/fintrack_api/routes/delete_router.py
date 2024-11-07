from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from fintrack_api.services.CRUD.delete import delete_item
from fintrack_api.services.CRUD.read import get_all_items_from_db
from fintrack_api.utils.frintrack_api_utils import validate_email_format


# -------------------- DELETE ROUTES -------------------- #

delete_router = APIRouter(prefix="/delete", tags=["Delete"])

EMAIL_REQUIRED = "The 'email' parameter is required."
EMAIL_NOT_FOUND = "Email not found"


@delete_router.delete("/revenue")
async def delete_revenue(email: Optional[str] = Query(None)):
    """
    Delete a revenue entry by email.

    Args:
        email (str, optional): The email associated with the revenue entry to be deleted.

    Returns:
        dict: A message indicating the result of the deletion process.

    Raises:
        HTTPException: If the email is missing, invalid, or no revenue entries are found.
    """
    # Check if the email parameter is provided
    if email is None:
        raise HTTPException(status_code=400, detail=EMAIL_REQUIRED)

    # Validate the email format and check if there are matching entries in the database
    if email:
        validate_email_format(email)

        # Query the database using the provided email
        revenues = await get_all_items_from_db("revenue", email)
        if not revenues:
            raise HTTPException(status_code=404, detail=EMAIL_NOT_FOUND)

        # Delete the revenue entry
        response = await delete_item("revenue", email)

    return {"message": response}


@delete_router.delete("/expenditure")
async def delete_expenditure(email: Optional[str] = Query(None)):
    """
    Delete an expenditure entry by email.

    Args:
        email (str, optional): The email associated with the expenditure entry to be deleted.

    Returns:
        dict: A message indicating the result of the deletion process.

    Raises:
        HTTPException: If the email is missing, invalid, or no expenditure entries are found.
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

        # Delete the expenditure entry
        response = await delete_item("expenditure", email)

    return {"message": response}


@delete_router.delete("/alert")
async def delete_alert(email: Optional[str] = Query(None)):
    """
    Delete an alert entry by email.

    Args:
        email (str, optional): The email associated with the alert entry to be deleted.

    Returns:
        dict: A message indicating the result of the deletion process.

    Raises:
        HTTPException: If the email is missing, invalid, or no alert entries are found.
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

        # Delete the alert entry
        response = await delete_item("alert", email)

    return {"message": response}


@delete_router.delete("/reminder")
async def delete_reminder(email: Optional[str] = Query(None)):
    """
    Delete a reminder entry by email.

    Args:
        email (str, optional): The email associated with the reminder entry to be deleted.

    Returns:
        dict: A message indicating the result of the deletion process.

    Raises:
        HTTPException: If the email is missing, invalid, or no reminder entries are found.
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

        # Delete the reminder entry
        response = await delete_item("reminder", email)

    return {"message": response}
