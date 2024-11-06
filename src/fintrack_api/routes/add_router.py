from typing import Dict
from fastapi import APIRouter, HTTPException
from fintrack_api.services.CRUD.create import AddItem, add_item_to_db
from fintrack_api.utils.frintrack_api_utils import validate_email_format, email_exists, validate_infos

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

    validate_email_format(item.email_id)

    validate_infos(item)

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

    validate_email_format(item.email_id)

    validate_infos(item)

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
    validate_email_format(item.email_id)

    validate_infos(item)

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

    validate_email_format(item.email_id)

    validate_infos(item)

    return await add_item_to_db("reminder", item)
