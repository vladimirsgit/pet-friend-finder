from pydantic import BaseModel, EmailStr


class SignUpRequest(BaseModel):
    email: EmailStr
    username: str
    password: str
    confirm_password: str