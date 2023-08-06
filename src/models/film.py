import datetime
import uuid
from typing import Optional, List

from pydantic import BaseModel


class Film(BaseModel):
    """
    Represents a film.

    Attributes:
    - id (UUID): Unique identifier
    - title (str): The title of the film.
    - description (Optional[str]): The description of the film (if available).
    - creation_date (Optional[datetime.date]): The creation date of the film (if available).
    - source_link (Optional[str]): The source link of the film (if available).
    - actors (Optional[List[Person]]): List of actors associated with the film (if available).
    - screen_writers (Optional[List[Person]]): List of screenwriters associated with the film (if available).
    - directors (Optional[List[Person]]): List of directors associated with the film (if available).
    - genres (Optional[List[Genre]]): List of genres associated with the film (if available).
    """

    id: uuid.UUID
    title: str
    description: Optional[str]
    creation_date: Optional[datetime.date]
    source_link: Optional[str]
    actors: Optional[List["Person"]]
    screen_writers: Optional[List["Person"]]
    directors: Optional[List["Person"]]
    genres: Optional[List["Genre"]]
