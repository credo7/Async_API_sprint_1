from typing import List, Optional
import uuid

from pydantic import BaseModel, model_validator


class PersonFilms(BaseModel):
    """
    Attributes:
        - id (str):
        - roles (list[optional[str]]):
    """

    id: str
    roles: List[Optional[str]] = []


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
