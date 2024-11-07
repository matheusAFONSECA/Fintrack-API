import re
from fastapi import HTTPException
from passlib.context import CryptContext
from fintrack_api.services.CRUD.create import AddItem
from fintrack_api.services.db import connect

# Initialize the bcrypt context for password hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Generate a bcrypt hash for the given password.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The bcrypt hash of the password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify that the plain text password matches the hashed password.

    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password to verify against.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def validate_password_strength(password: str) -> None:
    """
    Validate the strength of the given password.

    Args:
        password (str): The password to validate.

    Raises:
        HTTPException: If the password is less than 6 characters long.
    """
    if len(password) < 6:
        raise HTTPException(
            status_code=400,
            detail="The password must be at least 6 characters long.",
        )


def validate_email_format(email: str) -> None:
    """
    Validate the format of the given email address.

    Args:
        email (str): The email address to validate.

    Raises:
        ValueError: If the email format is invalid.
    """
    pattern = r"^[\w\.-]+@[\w\.-]+\.(com|br)$"
    if not re.match(pattern, email):
        raise HTTPException(
            status_code=400,
            detail="The email must be in the format 'name@domain.com' or 'name@domain.br'.",
        )


def email_exists(email):
    """
    Check if the email already exists in the database.

    Args:
        email (str): The email address to check.

    Returns:
        bool: True if the email exists, False otherwise.
    """
    query = """
        SELECT u.email
        FROM "user" u
        WHERE u.email = %(email)s;
    """

    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, {"email": email})
            result = cursor.fetchone()

            if result:
                print(f"Query result: {result}")  # Debug
                return True
            print("No user found.")  # Debug
            return None


def validate_infos(item: AddItem):
    """
    Validates the information in an AddItem object before processing.

    Args:
        item (AddItem): An object containing item information to be validated.

    Raises:
        HTTPException: If any validation fails, an HTTPException is raised with a specific error message.
    """
    # Validate the existence of the email
    if not email_exists(item.email_id):
        raise HTTPException(
            status_code=404, detail="This email does not exist in the database."
        )

    # Validate the value
    if item.value <= 0:
        raise HTTPException(
            status_code=400, detail="The value must be greater than zero."
        )

    # Validate the date
    if not item.date:
        raise HTTPException(
            status_code=400, detail="The date is required for the alert."
        )
