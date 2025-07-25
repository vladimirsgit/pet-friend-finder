import uuid

from datetime import datetime

from pydantic import BaseModel, EmailStr

class UserDTO(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    password: str
    confirmed: bool
    created_at: datetime

