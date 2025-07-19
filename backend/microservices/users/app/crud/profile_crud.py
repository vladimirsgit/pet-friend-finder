from app.crud.base_crud import BaseCRUD
from app.model.profile import Profile

from typing import Optional

from sqlmodel import select

class ProfileCRUD(BaseCRUD):
    async def save(self, profile: Profile):
        self.db.add(profile)
        await self.db.commit()