from fastapi import Depends

from app.core.constants import constants
from app.crud.user_crud import UserCRUD
from app.model.user import User
from app.schema.signup_request import SignUpRequest

class UserService:
    def __init__(self, user_crud: UserCRUD = Depends(UserCRUD)):
        self.user_crud = user_crud

    async def check_if_username_exists(self, username: str) -> bool:
        return await self.user_crud.check_if_username_exists(username)

    async def signup(self, signup_request: SignUpRequest):
        await self.user_crud.save(User(email=signup_request.email, username=signup_request.username, password=signup_request.hashed_password))



    async def __validate_signup_password(self, password, confirm_password):
        if password != confirm_password:
            raise ValueError('Passwords do not match')
        if len(password) < constants.PASS_MIN_LENGTH or len(password) > constants.PASS_MAX_LENGTH:
            raise ValueError(f'Password must be at least {constants.PASS_MIN_LEN} characters and at most {constants.PASS_MAX_LEN} characters.')

