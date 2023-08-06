import uuid
from typing import Optional

from pydantic import BaseModel


class Genre(BaseModel):
    """
    Represents a genre associated with a film

    Attributes:
        - id (UUID): Unique identifier
        - name (str): The name of genre
        - description (str): The description of genre (if available)
    """

    id: uuid.UUID
    name: str
    description: Optional[str]
