import uuid

import logging

from app.crud.base_crud import BaseCRUD
from app.exception.profile_not_found_error import ProfileNotFoundError
from app.model.profile import Profile

from typing import Optional

from sqlmodel import select

from app.schema.profile_dto import ProfileDTO

logger = logging.getLogger(__name__)

class ProfileCRUD(BaseCRUD):

    async def get_profile_by_user_id(self, user_id: uuid.UUID) -> Profile:
        stmt = select(Profile).where(Profile.user_id == user_id)
        res = await self.db.execute(stmt)
        profile: Optional[Profile] = res.scalar_one_or_none()

        if not profile:
            profile_not_found_error = ProfileNotFoundError()
            logger.error(profile_not_found_error.message)
            raise profile_not_found_error

        return profile

    async def save(self, profile: Profile):
        self.db.add(profile)
        await self.db.commit()

    async def update(self, profile: ProfileDTO, user_id: uuid.UUID):
        old_profile: Optional[Profile] = await self.get_profile_by_user_id(user_id=user_id)
        for field in ProfileDTO.model_fields.keys():
            setattr(old_profile, field, getattr(profile, field))

        self.db.add(old_profile)
        await self.db.commit()

    async def check_if_profile_exists_by_user_id(self, user_id: uuid.UUID) -> bool:
        stmt = select(1).where(Profile.user_id == user_id)

        res = await self.db.execute(stmt)

        return bool(res.scalar_one_or_none())