from pydantic import BaseModel, EmailStr


class SignUpRequestHashedPass(BaseModel):
    email: EmailStr
    username: str
    hashed_password: str