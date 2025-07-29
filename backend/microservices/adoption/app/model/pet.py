import uuid

from sqlmodel import SQLModel, Field

from app.enum.gender import Gender


class Pet(SQLModel, table=True):
    __tablename__ = 'pet'
    __table_args__ = {"schema": "adoptions_svc"}

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=100, nullable=False)
    type: str = Field(max_length=50, nullable=False)
    breed: str = Field(max_length=100, nullable=False)
    age: int = Field(nullable=False)
    gender: Gender = Field(nullable=False)
    description: str = Field(max_length=1000, nullable=False)
    vaccinated: bool = Field(nullable=False)
    neutered: bool = Field(nullable=False)
    owner_id: uuid.UUID = Field(nullable=False)