import uuid
from typing import Optional

import aio_pika.abc

from fastapi import Depends

from app.core.rabbitmq_client import rabbit_client, RabbitMQClient
from app.crud.profile_crud import ProfileCRUD
from app.exception.profile_not_found_error import ProfileNotFoundError
from app.model.profile import Profile
from app.schema.profile_dto import ProfileDTO

from app.core.constants import constants

class ProfileService:
    def __init__(self, profile_crud: ProfileCRUD = Depends(ProfileCRUD),
                        rabbit_c: aio_pika.abc.AbstractChannel = Depends(rabbit_client)):
        self.profile_crud = profile_crud
        self.rabbit_c = rabbit_c

    async def create(self, profile: ProfileDTO, user_id: uuid.UUID):
        # TODO fix this check logic
        try:
            await self.get_profile(user_id)
        except ProfileNotFoundError:
            await self.profile_crud.save(Profile(user_id=user_id,
                                                 first_name=profile.first_name,
                                                 last_name=profile.last_name,
                                                 bio=profile.bio,
                                                 latitude=profile.latitude,
                                                 longitude=profile.longitude,
                                                 age=profile.age,
                                                 gender=profile.gender,
                                                 phone_number=profile.phone_number))

            return
        await self.rabbit_c.default_exchange.publish(
            aio_pika.Message(
                body='Hello, this is my first rabbitmq published message! :)'.encode()
            ),
            routing_key=constants.PET_SUGGESTION_QUEUE_NAME
        )


    async def update(self, profile: ProfileDTO, user_id: uuid.UUID):
        await self.profile_crud.update(profile, user_id)

    async def get_profile(self, user_id: uuid.UUID) -> Profile:
        return await self.profile_crud.get_profile_by_user_id(user_id)