import uuid

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

class UserSuggestDTO(BaseModel):
    id: uuid.UUID
    bio: str
    latitude: float
    longitude: float
