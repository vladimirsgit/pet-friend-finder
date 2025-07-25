import uuid
from typing import Optional

from fastapi import Depends

from app.crud.profile_crud import ProfileCRUD
from app.model.profile import Profile
from app.schema.profile_dto import ProfileDTO


class ProfileService:
    def __init__(self, profile_crud: ProfileCRUD = Depends(ProfileCRUD)):
        self.profile_crud = profile_crud

    async def create(self, profile: ProfileDTO, user_id: uuid.UUID):
        await self.profile_crud.save(Profile(user_id=user_id,
                                             first_name=profile.first_name,
                                             last_name=profile.last_name,
                                             bio=profile.bio,
                                             latitude=profile.latitude,
                                             longitude=profile.longitude,
                                             age=profile.age,
                                             gender=profile.gender,
                                             phone_number=profile.phone_number))
    async def update(self, profile: ProfileDTO, user_id: uuid.UUID):
        await self.profile_crud.update(profile, user_id)

    async def get_profile(self, user_id: uuid.UUID) -> Profile:
        return await self.profile_crud.get_profile_by_user_id(user_id)