from typing import List, Optional

from pydantic import BaseModel


class PersonFilms(BaseModel):
    """
    Attributes:
        - id (str):
        - roles (list[optional[str]]):
    """

    id: str
    roles: List[Optional[str]] = []


class Person(BaseModel):
    """
    Represents a person associated with a film.

    Attributes:
    - id (UUID): Unique identifier
    - name (str): The name of the person.
    - films (Optional[List[PersonFilms]]): List of films associated with the film (if available).

    """

    id: str
    full_name: str
    films: Optional[List['PersonFilms']]
