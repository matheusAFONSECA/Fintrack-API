from typing import Optional
from fastapi import HTTPException
from fastapi import APIRouter, Query
from fintrack_api.services.CRUD.read import get_all_items_from_db
from fintrack_api.utils.frintrack_api_utils import validate_email_format


# -------------------- VISUALIZATION ROUTES -------------------- #

visualization_router = APIRouter(prefix="/visualization", tags=["Visualization"])

EMAIL_REQUIRED = "The 'email' parameter is required."
EMAIL_NOT_FOUND = "Email not found"


@visualization_router.get("/revenue")
async def get_all_revenue(email: Optional[str] = Query(None)):
    """
    Retrieve all revenue entries, optionally filtered by email.

    Args:
        email (Optional[str]): The email to filter the results by (if provided).

    Returns:
        List[Dict[str, str]]: A list of revenue entries.
    """

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

    return {"revenues": revenues}


@visualization_router.get("/expenditure")
async def get_all_expenditure(email: Optional[str] = Query(None)):
    """
    Retrieve all expenditure entries, optionally filtered by email.

    Args:
        email (Optional[str]): The email to filter the results by (if provided).

    Returns:
        List[Dict[str, str]]: A list of expenditure entries.
    """
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

    return {"expenditures": expenditures}


@visualization_router.get("/alert")
async def get_all_alerts(email: Optional[str] = Query(None)):
    """
    Retrieve all alert entries, optionally filtered by email.

    Args:
        email (Optional[str]): The email to filter the results by (if provided).

    Returns:
        List[Dict[str, str]]: A list of alert entries.
    """

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

    return {"alerts": alerts}


@visualization_router.get("/reminder")
async def get_all_reminders(email: Optional[str] = Query(None)):
    """
    Retrieve all reminder entries, optionally filtered by email.

    Args:
        email (Optional[str]): The email to filter the results by (if provided).

    Returns:
        List[Dict[str, str]]: A list of reminder entries.
    """
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

    return {"reminders": reminders}
