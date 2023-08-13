import uuid
from typing import Optional

from pydantic import BaseModel, model_validator


class MoviePerson(BaseModel):
    """
    Represents a person associated with a film.

    Attributes:
    - id (Str): Unique identifier.
    - name (str): The name of the person.
    """

    id: str
    full_name: str


class MoviePersonName(BaseModel):
    """
        Represents a short version of person associated with a film.

        Attributes:
        - name (str): The name of the person.
        """

    full_name: str
