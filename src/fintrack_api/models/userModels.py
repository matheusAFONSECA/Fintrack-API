from typing import Optional
from pydantic import BaseModel, Field


class UserOut(BaseModel):
    """
    Output model to display user data.

    Attributes:
        name (str): The name of the user (up to 150 characters).
        email (str): The email of the user (up to 100 characters).
    """

    name: str = Field(..., max_length=150)
    email: str = Field(..., max_length=100)


class UserIn(UserOut):
    """
    Input model for registering a new user.

    Attributes:
        password (str): The user's password (up to 64 characters).
    """

    password: str = Field(..., max_length=64)


class UserInDB(BaseModel):
    """
    Model representing a user stored in the database.

    Attributes:
        name (str): The name of the user.
        email (str): The email of the user.
        password (str): The hashed password of the user.
    """

    name: str
    email: str
    password: str


class UserInQuery(BaseModel):
    """
    Model representing optional query parameters for user searches.

    Attributes:
        name (Optional[str]): The name of the user (up to 150 characters).
        email (Optional[str]): The email of the user (up to 100 characters).
        phone (Optional[str]): The phone number of the user (up to 15 characters).
        birth (Optional[str]): The user's date of birth in the format 'DD/MM/YYYY'.
    """

    name: Optional[str] = Field(None, max_length=150)
    email: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=15)
    birth: Optional[str] = Field(None, max_length=10)
