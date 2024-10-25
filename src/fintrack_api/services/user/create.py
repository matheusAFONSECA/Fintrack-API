from fintrack_api.utils.frintrack_api_utils import get_password_hash
from fintrack_api.models.userModels import UserIn
from fintrack_api.services.db import connect
from fastapi import HTTPException


async def create_user(user: UserIn) -> None:
    query = """
        INSERT INTO "user" (name, email, password)
        VALUES (%(name)s, %(email)s, %(password)s);
    """
    parameters = {
        "name": user.name,
        "email": user.email,
        "password": get_password_hash(user.password),
    }
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, parameters)
            conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
