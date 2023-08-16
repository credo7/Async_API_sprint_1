from models.base import BaseConfig


class PersonFilms(BaseConfig):
    """
    Attributes:
        - id (str):
        - roles (List[str | None]):
    """

    id: str
    roles: list[str | None] = []


class MoviePerson(BaseConfig):
    """
    Represents a person associated with a film.

    Attributes:
    - id (Str): Unique identifier.
    - full_name (str): The name of the person.
    """

    id: str
    full_name: str


class MoviePersonName(BaseConfig):
    """
    Represents a short version of person associated with a film.

    Attributes:
    - full_name (str): The full_name of the person.
    """

    full_name: str


class Person(BaseConfig):
    """
    Represents a person associated with a film.

    Attributes:
    - id (UUID): Unique identifier
    - full_name (str): The full_name of the person.
    - films (Optional[List[PersonFilms]]): List of films associated with the film (if available).

    """

    id: str
    full_name: str
    films: list["PersonFilms"] | None
