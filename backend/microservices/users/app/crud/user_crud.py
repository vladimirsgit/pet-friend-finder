import uuid

from app.crud.base_crud import BaseCRUD
from app.model.user import User

from typing import Optional

from sqlmodel import select

class UserCRUD(BaseCRUD):
    async def get_user_by_username(self, username: str) -> Optional[User]:
        stmt = select(User).where(User.username == username)

        res = await self.db.execute(stmt)

        return res.scalar_one_or_none()

    async def check_if_username_exists(self, username: str) -> bool:
        stmt = select(1).where(User.username == username)

        res = await self.db.execute(stmt)

        return bool(res.scalar_one_or_none())

    async def save(self, user: User):
        self.db.add(user)
        await self.db.commit()
