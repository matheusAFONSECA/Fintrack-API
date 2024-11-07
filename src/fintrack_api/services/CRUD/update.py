from fastapi import HTTPException
from src.fintrack_api.services.db import connect


async def update_revenue_by_email(email: str, updated_data: dict) -> dict:
    """Update a revenue entry by email."""
    return await update_item("revenue", email, updated_data)


async def update_expenditure_by_email(email: str, updated_data: dict) -> dict:
    """Update an expenditure entry by email."""
    return await update_item("expenditure", email, updated_data)


async def update_alert_by_email(email: str, updated_data: dict) -> dict:
    """Update an alert entry by email."""
    return await update_item("alert", email, updated_data)


async def update_reminder_by_email(email: str, updated_data: dict) -> dict:
    """Update a reminder entry by email."""
    return await update_item("reminder", email, updated_data)


async def update_item(table: str, email: str, updated_data: dict) -> dict:
    """Helper function to update an item in a specified table by email."""
    set_clause = ", ".join([f"{key} = %({key})s" for key in updated_data.keys()])
    query = f"""
        UPDATE {table} SET {set_clause}
        WHERE email_id = %(email)s;
    """
    parameters = {"email": email, **updated_data}

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, parameters)
            conn.commit()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return {"message": f"{table.capitalize()} updated successfully!"}
