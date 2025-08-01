import uuid

from pydantic import BaseModel, Field

from typing import Optional


from datetime import datetime

from app.enum.gender import Gender

from app.core.constants import constants


class ProfileDTO(BaseModel):
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    bio: str = Field(max_length=1000)
    latitude: float
    longitude: float
    age: int = Field(ge=14, le=120)
    gender: Gender
    phone_number: str = Field(max_length=50)