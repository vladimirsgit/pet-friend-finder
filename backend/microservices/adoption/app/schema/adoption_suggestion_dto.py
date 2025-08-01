import uuid
from typing import List

from pydantic import BaseModel, Field

class AdoptionSuggestionDTO(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: uuid.UUID
    suggestions: List[uuid.UUID]