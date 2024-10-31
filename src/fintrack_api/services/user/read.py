from typing import List, Optional
from fastapi import HTTPException
from src.fintrack_api.services.db import connect
from src.fintrack_api.models.userModels import UserOut, UserInDB


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
    print(f"Executing query for email: {email}")  # Debug

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, {"email": email})
                result = cursor.fetchone()

                if result:
                    print(f"Query result: {result}")  # Debug
                    return UserInDB(password=result[0], email=result[1], name=result[2])
                print("No user found.")  # Debug
                return None
    except Exception as e:
        print(f"Error retrieving user: {e}")  # Debug
        raise HTTPException(status_code=500, detail=str(e))
