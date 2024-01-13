#!/usr/bin/python3
"""The script defines the Review class."""
from models.base_model import BaseModel


class Review(BaseModel):
    """Represents a review.

    Attributes:
        place_id (str): the Place id.
        user_id (str): the User id.
        text (str): the text of the review.
    """

    place_id = ""
    user_id = ""
    text = ""
