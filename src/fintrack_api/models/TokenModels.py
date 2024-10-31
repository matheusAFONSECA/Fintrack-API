from typing import Union
from pydantic import BaseModel


class Token(BaseModel):
    """
    Model representing an access token.

    Attributes:
        access_token (str): The actual access token string.
        token_type (str): The type of the token (e.g., "bearer").
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Model representing token data, including the user ID.

    Attributes:
        user_id (Union[str, None]): The user ID associated with the token. Can be None if not provided.
    """

    user_id: Union[str, None] = None
