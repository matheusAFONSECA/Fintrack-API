from fastapi import HTTPException
from fintrack_api.services.db import connect


async def delete_revenue_by_email(email: str) -> dict:
    """Delete a revenue entry by email."""
    return await delete_item("revenue", email)


async def delete_expenditure_by_email(email: str) -> dict:
    """Delete an expenditure entry by email."""
    return await delete_item("expenditure", email)


async def delete_alert_by_email(email: str) -> dict:
    """Delete an alert entry by email."""
    return await delete_item("alert", email)


async def delete_reminder_by_email(email: str) -> dict:
    """Delete a reminder entry by email."""
    return await delete_item("reminder", email)


async def delete_item(table: str, email: str) -> dict:
    """Helper function to delete an item from a specified table by email."""
    query = f"""
        DELETE FROM {table}
        WHERE email_id = %(email)s;
    """
    parameters = {"email": email}

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, parameters)
            conn.commit()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return {"message": f"{table.capitalize()} deleted successfully!"}
