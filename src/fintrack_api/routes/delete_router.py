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
    """Delete a revenue entry by email."""
    # Verifica se o parâmetro email foi passado
    if email is None:
        raise HTTPException(status_code=400, detail=EMAIL_REQUIRED)

    # Verifica se o parâmetro email foi passado e se é válido
    if email:
        validate_email_format(email)  # Valida o formato do e-mail

        # Consulta o banco de dados usando o email
        revenues = await get_all_items_from_db("revenue", email)
        if not revenues:
            raise HTTPException(status_code=404, detail=EMAIL_NOT_FOUND)

        # Deleta a receita
        response = await delete_item("revenue", email)

    return {"message": response}


@delete_router.delete("/expenditure")
async def delete_expenditure(email: Optional[str] = Query(None)):
    """Delete an expenditure entry by email."""
    # Verifica se o parâmetro email foi passado
    if email is None:
        raise HTTPException(status_code=400, detail=EMAIL_REQUIRED)

    # Verifica se o parâmetro email foi passado e se é válido
    if email:
        validate_email_format(email)  # Valida o formato do e-mail

        # Consulta o banco de dados usando o email
        expenditures = await get_all_items_from_db("expenditure", email)
        if not expenditures:
            raise HTTPException(status_code=404, detail=EMAIL_NOT_FOUND)

        # Deleta a despesa
        response = await delete_item("expenditure", email)

    return {"message": response}


@delete_router.delete("/alert")
async def delete_alert(email: Optional[str] = Query(None)):
    """Delete an alert entry by email."""
    # Verifica se o parâmetro email foi passado
    if email is None:
        raise HTTPException(status_code=400, detail=EMAIL_REQUIRED)

    # Verifica se o parâmetro email foi passado e se é válido
    if email:
        validate_email_format(email)  # Valida o formato do e-mail

        # Consulta o banco de dados usando o email
        alerts = await get_all_items_from_db("alert", email)
        if not alerts:
            raise HTTPException(status_code=404, detail=EMAIL_NOT_FOUND)

        # Deleta o alerta
        response = await delete_item("alert", email)

    return {"message": response}


@delete_router.delete("/reminder")
async def delete_reminder(email: Optional[str] = Query(None)):
    """Delete a reminder entry by email."""
    # Verifica se o parâmetro email foi passado
    if email is None:
        raise HTTPException(status_code=400, detail=EMAIL_REQUIRED)

    # Verifica se o parâmetro email foi passado e se é válido
    if email:
        validate_email_format(email)  # Valida o formato do e-mail

        # Consulta o banco de dados usando o email
        reminders = await get_all_items_from_db("reminder", email)
        if not reminders:
            raise HTTPException(status_code=404, detail=EMAIL_NOT_FOUND)

        # Deleta o lembrete
        response = await delete_item("reminder", email)

    return {"message": response}
