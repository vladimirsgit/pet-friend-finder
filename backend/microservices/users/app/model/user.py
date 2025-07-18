import uuid

from pydantic import EmailStr

from typing import Optional

from sqlmodel import SQLModel, Field

from datetime import datetime

from app.core.constants import constants


class User(SQLModel, table=True):
    __tablename__ = 'users'
    __table_args__ = {"schema": "users_svc"}

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(unique=True, max_length=constants.USERNAME_MAX_LEN)
    email: EmailStr = Field(nullable=False)
    password: str = Field(nullable=False, min_length=constants.PASS_MIN_LEN, max_length=constants.PASS_MAX_LEN)
    confirmed: bool = Field(nullable=False, default=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

