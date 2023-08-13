from pydantic import BaseModel


class Genre(BaseModel):
    """
    Represents a genre associated with a film

    Attributes:
        - name (str): The name of genre
    """

    name: str
