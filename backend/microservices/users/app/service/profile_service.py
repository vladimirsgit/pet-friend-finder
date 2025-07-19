from fastapi import Depends

from app.crud.profile_crud import ProfileCRUD
from app.model.profile import Profile
from app.schema.profile_dto import ProfileDTO


class ProfileService:
    def __init__(self, profile_crud: ProfileCRUD = Depends(ProfileCRUD)):
        self.profile_crud = profile_crud

    async def save(self, profile: ProfileDTO):
        await self.profile_crud.save(profile)