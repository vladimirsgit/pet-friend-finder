import uuid

from pydantic import EmailStr

from typing import Optional

from sqlmodel import SQLModel, Field

from datetime import datetime

from app.enum.gender import Gender

from app.core.constants import constants


class Profile(SQLModel, table=True):
    __tablename__ = 'profiles'
    __table_args__ = {"schema": "users_svc"}

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users_svc.users.id")
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    bio: str = Field(nullable=False)
    latitude: float = Field(nullable=False)
    longitude: float = Field(nullable=False)
    age: int = Field(nullable=False)
    gender: Gender = Field(nullable=False)
    phone_number: str = Field(nullable=False)