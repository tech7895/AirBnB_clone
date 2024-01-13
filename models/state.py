#!/usr/bin/python3
"""The script defines the State class."""
from models.base_model import BaseModel


class State(BaseModel):
    """Represents a state.

    Attributes:
        name (str): the name of the state.
    """

    name = ""
