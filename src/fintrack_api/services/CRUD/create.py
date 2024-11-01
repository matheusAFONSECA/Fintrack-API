from pydantic import BaseModel
from fastapi import HTTPException
from fintrack_api.services.db import connect
from fintrack_api.models.userModels import UserIn


class AddItem(BaseModel):
    email_id: str
    item_type: str
    value: float
    annotation: str
    date: str


async def create_user(user: UserIn) -> None:
    """
    Register a new user in the database with a hashed password.

    Args:
        user (UserIn): The user data containing name, email, and password.

    Raises:
        HTTPException: If an error occurs during the database operation.
    """
    query = """
        INSERT INTO "user" (name, email, password)
        VALUES (%(name)s, %(email)s, %(password)s);
    """
    hashed_password = user.password

    parameters = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
    }

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, parameters)
            conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def add_item_to_db(table: str, item: AddItem):
    """Insert an item into the specified table."""
    query = f"""
        INSERT INTO {table} (email_id, type, value, annotation, date)
        VALUES (%(email_id)s, %(item_type)s, %(value)s, %(annotation)s, %(date)s);
    """
    parameters = item.dict()

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, parameters)
            conn.commit()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return {"message": f"{table.capitalize()} added successfully!"}
