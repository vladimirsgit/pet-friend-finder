import uuid

from pydantic import BaseModel

from app.enum.gender import Gender


class PetCreate(BaseModel):
    name: str
    type: str
    breed: str
    age: int
    gender: Gender
    description: str
    vaccinated: bool
    neutered: bool
    latitude: float
    longitude: float
