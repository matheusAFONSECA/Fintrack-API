from fastapi import HTTPException
from typing import Dict, List, Optional
from fintrack_api.services.db import connect
from fintrack_api.models.userModels import UserOut, UserInDB


async def get_all_users() -> Optional[List[UserOut]]:
    """
    Retrieve all users from the database.

    Returns:
        Optional[List[UserOut]]: A list of user details if users are found,
        otherwise None.

    Raises:
        HTTPException: If an error occurs during database access.
    """
    query = """
        SELECT u.name, u.email FROM "user" as u;
    """

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()

                if results:
                    users: List[UserOut] = [
                        UserOut(name=result[0], email=result[1]) for result in results
                    ]
                    return users
                return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


async def get_user_by_email_for_auth(email: str) -> Optional[UserInDB]:
    """
    Retrieve a user from the database by email for authentication.

    Args:
        email (str): The email of the user to retrieve.

    Returns:
        Optional[UserInDB]: A UserInDB object if the user is found,
        otherwise None.

    Raises:
        HTTPException: If an error occurs during database access.
    """
    query = """
        SELECT u.password, u.email, u.name
        FROM "user" u
        WHERE u.email = %(email)s;
    """

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, {"email": email})
                result = cursor.fetchone()

                if result:
                    return UserInDB(password=result[0], email=result[1], name=result[2])
                return None
    except Exception as e:
        print(f"Error retrieving user: {e}")  # Debug
        raise HTTPException(status_code=500, detail=str(e))


async def get_all_items_from_db(
    table: str, email: Optional[str] = None
) -> List[Dict[str, str]]:
    """
    Retrieve all items from the specified table, optionally filtered by email.

    Args:
        table (str): The name of the table to retrieve data from.
        email (Optional[str]): The email to filter the results by (if provided).

    Returns:
        List[Dict[str, str]]: A list of dictionary items representing the records.

    Raises:
        HTTPException: If an error occurs during database access.
    """
    if email:
        query = f"SELECT * FROM {table} WHERE email_id = %(email)s;"
        parameters = {"email": email}
    else:
        query = f"SELECT * FROM {table};"
        parameters = {}

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, parameters)
                results = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                return [dict(zip(columns, row)) for row in results]
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
