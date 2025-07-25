import uuid

from app.crud.base_crud import BaseCRUD
from app.model.profile import Profile

from typing import Optional

from sqlmodel import select

from app.schema.profile_dto import ProfileDTO


class ProfileCRUD(BaseCRUD):

    async def get_profile_by_user_id(self, user_id: uuid.UUID) -> Optional[Profile]:
        stmt = select(Profile).where(Profile.user_id == user_id)
        res = await self.db.execute(stmt)

        return res.scalar_one_or_none()

    async def save(self, profile: Profile):
        self.db.add(profile)
        await self.db.commit()

    async def update(self, profile: ProfileDTO, user_id: uuid.UUID):
        old_profile: Optional[Profile] = await self.get_profile_by_user_id(user_id=user_id)
        for field in ProfileDTO.model_fields.keys():
            setattr(old_profile, field, getattr(profile, field))

        self.db.add(old_profile)
        await self.db.commit()