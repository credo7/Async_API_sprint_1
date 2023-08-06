import uuid
from typing import List, Optional

from pydantic import BaseModel


class Person(BaseModel):
    """
    Represents a person associated with a film.

    Attributes:
    - id (UUID): Unique identifier
    - name (str): The name of the person.
    - films (Optional[List[Film]]): List of films associated with the film (if available).

    """

    id: uuid.UUID
    full_name: str
    films: Optional[List["Film"]]
