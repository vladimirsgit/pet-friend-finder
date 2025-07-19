from typing import Optional

from fastapi import Depends

from app.core.constants import constants
from app.crud.user_crud import UserCRUD
from app.exception.user_not_found_error import UserNotFoundError
from app.model.user import User
from app.schema.signup_request import SignUpRequest

class UserService:
    def __init__(self, user_crud: UserCRUD = Depends(UserCRUD)):
        self.user_crud = user_crud

    async def check_if_username_exists(self, username: str) -> bool:
        return await self.user_crud.check_if_username_exists(username)

    async def signup(self, signup_request: SignUpRequest):
        await self.user_crud.save(User(email=signup_request.email, username=signup_request.username, password=signup_request.hashed_password))

    async def confirm_email(self, username: str):
        user: Optional[User] = await self.user_crud.get_user_by_username(username)
        if user is None:
            raise UserNotFoundError()
        user.confirmed = True
        await self.user_crud.save(user)

    async def read_user(self, username: str) -> User:
        user: Optional[User] = await self.user_crud.get_user_by_username(username)
        if user is None:
            raise UserNotFoundError()
        return user