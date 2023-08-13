from typing import Optional

from pydantic import BaseModel


class Genre(BaseModel):
    """
    Represents a genre associated with a film

    Attributes:
        - id (str): Unique identifier
        - name (str): The name of genre
        - description (str): The description of genre (if available)
    """

    id: str
    name: str
    description: Optional[str]
