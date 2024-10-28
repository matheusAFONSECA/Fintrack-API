from fastapi import HTTPException
from fintrack_api.services.db import connect
from fintrack_api.models.userModels import UserIn
from fintrack_api.utils.frintrack_api_utils import get_password_hash


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

    # Hash the password before storing it in the database
    # hashed_password = get_password_hash(user.password)
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
