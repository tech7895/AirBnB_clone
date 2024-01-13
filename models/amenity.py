#!/usr/bin/python3
"""The script defines the Amenity class."""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Represents an amenity

    Attributes:
        name (str): the name of the amenity.
    """

    name = ""
