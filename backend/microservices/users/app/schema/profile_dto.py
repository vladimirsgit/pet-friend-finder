import uuid

from pydantic import BaseModel

from typing import Optional


from datetime import datetime

from app.enum.gender import Gender

from app.core.constants import constants


class ProfileDTO(BaseModel):
    first_name: str
    last_name: str
    bio: str
    latitude: float
    longitude: float
    age: int
    gender: Gender
    phone_number: str