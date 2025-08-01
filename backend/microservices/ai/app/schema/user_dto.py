import uuid

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

class UserDTO(BaseModel):
    id: uuid.UUID
    username: str = Field(max_length=50)
    email: EmailStr
    password: str
    confirmed: bool
    created_at: datetime

