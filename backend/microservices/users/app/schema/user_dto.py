import uuid

from datetime import datetime

from pydantic import BaseModel, EmailStr

class UserDTO(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirmed: bool
    created_at: datetime

