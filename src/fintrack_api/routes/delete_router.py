from fastapi import APIRouter
from fintrack_api.services.CRUD.delete import (
    delete_revenue_by_email,
    delete_expenditure_by_email,
    delete_alert_by_email,
    delete_reminder_by_email,
)

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