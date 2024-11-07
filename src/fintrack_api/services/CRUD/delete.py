from fastapi import HTTPException
from src.fintrack_api.services.db import connect


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

    return f"{table.capitalize()} deleted successfully."
