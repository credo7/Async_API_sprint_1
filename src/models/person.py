import uuid
from typing import Optional

from pydantic import BaseModel, model_validator


class Person(BaseModel):
    """
    Represents a person associated with a film.

    Attributes:
    - id (Optional[UUID]): Unique identifier (if available).
    - name (str): The name of the person.
    - films (Optional[List[Film]]): List of films associated with the film (if available).

    """

    id: Optional[str]
    full_name: str

    @model_validator(mode='after')
    def _validate_uuid(self):
        try:
            if self.id is None:
                return None
            uuid.UUID(self.id)
            return self
        except ValueError:
            raise ValueError('Invalid UUID format')
