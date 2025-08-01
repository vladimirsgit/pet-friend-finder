import uuid

from pydantic import BaseModel

class PetDescDTO(BaseModel):
    id: uuid.UUID
    description: str

