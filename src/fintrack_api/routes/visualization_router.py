from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from src.fintrack_api.services.CRUD.read import get_all_items_from_db
from src.fintrack_api.utils.frintrack_api_utils import validate_email_format


# -------------------- VISUALIZATION ROUTES -------------------- #

visualization_router = APIRouter(prefix="/visualization", tags=["Visualization"])

EMAIL_REQUIRED = "The 'email' parameter is required."
EMAIL_NOT_FOUND = "Email not found"


@visualization_router.get("/revenue")
async def get_all_revenue(email: Optional[str] = Query(None)):
    """
    Retrieve all revenue entries, filtered by email if provided.

    Args:
        email (Optional[str]): The email to filter the results by (if provided).

    Returns:
        dict: A dictionary containing a list of revenue entries.

    Raises:
        HTTPException: If the email is missing, invalid, or no entries are found.
    """
    # Check if the email parameter is provided
    if email is None:
        raise HTTPException(status_code=400, detail=EMAIL_REQUIRED)

    # Validate email format and check for matching entries in the database
    if email:
        validate_email_format(email)

        # Query the database using the provided email
        revenues = await get_all_items_from_db("revenue", email)
        if not revenues:
            raise HTTPException(status_code=404, detail=EMAIL_NOT_FOUND)

    return {"revenues": revenues}


@visualization_router.get("/expenditure")
async def get_all_expenditure(email: Optional[str] = Query(None)):
    """
    Retrieve all expenditure entries, filtered by email if provided.

    Args:
        email (Optional[str]): The email to filter the results by (if provided).

    Returns:
        dict: A dictionary containing a list of expenditure entries.

    Raises:
        HTTPException: If the email is missing, invalid, or no entries are found.
    """
    # Check if the email parameter is provided
    if email is None:
        raise HTTPException(status_code=400, detail=EMAIL_REQUIRED)

    # Validate email format and check for matching entries in the database
    if email:
        validate_email_format(email)

        # Query the database using the provided email
        expenditures = await get_all_items_from_db("expenditure", email)
        if not expenditures:
            raise HTTPException(status_code=404, detail=EMAIL_NOT_FOUND)

    return {"expenditures": expenditures}


@visualization_router.get("/alert")
async def get_all_alerts(email: Optional[str] = Query(None)):
    """
    Retrieve all alert entries, filtered by email if provided.

    Args:
        email (Optional[str]): The email to filter the results by (if provided).

    Returns:
        dict: A dictionary containing a list of alert entries.

    Raises:
        HTTPException: If the email is missing, invalid, or no entries are found.
    """
    # Check if the email parameter is provided
    if email is None:
        raise HTTPException(status_code=400, detail=EMAIL_REQUIRED)

    # Validate email format and check for matching entries in the database
    if email:
        validate_email_format(email)

        # Query the database using the provided email
        alerts = await get_all_items_from_db("alert", email)
        if not alerts:
            raise HTTPException(status_code=404, detail=EMAIL_NOT_FOUND)

    return {"alerts": alerts}


@visualization_router.get("/reminder")
async def get_all_reminders(email: Optional[str] = Query(None)):
    """
    Retrieve all reminder entries, filtered by email if provided.

    Args:
        email (Optional[str]): The email to filter the results by (if provided).

    Returns:
        dict: A dictionary containing a list of reminder entries.

    Raises:
        HTTPException: If the email is missing, invalid, or no entries are found.
    """
    # Check if the email parameter is provided
    if email is None:
        raise HTTPException(status_code=400, detail=EMAIL_REQUIRED)

    # Validate email format and check for matching entries in the database
    if email:
        validate_email_format(email)

        # Query the database using the provided email
        reminders = await get_all_items_from_db("reminder", email)
        if not reminders:
            raise HTTPException(status_code=404, detail=EMAIL_NOT_FOUND)

    return {"reminders": reminders}
