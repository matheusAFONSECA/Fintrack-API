from fastapi import APIRouter
from fintrack_api.services.CRUD.update import (
    update_revenue_by_email,
    update_expenditure_by_email,
    update_alert_by_email,
    update_reminder_by_email,
)

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