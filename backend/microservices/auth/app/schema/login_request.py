from pydantic import BaseModel


class LogInRequest(BaseModel):
    username: str
    password: str
