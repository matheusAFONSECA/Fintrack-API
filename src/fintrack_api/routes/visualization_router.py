from typing import Optional
from fastapi import APIRouter, Query
from fintrack_api.services.CRUD.read import get_all_items_from_db


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
