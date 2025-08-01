import json
import uuid
from typing import Optional

import logging

import aio_pika.abc

from fastapi import Depends, BackgroundTasks

from app.core.rabbitmq_client import rabbit_client, RabbitMQClient
from app.crud.profile_crud import ProfileCRUD
from app.exception.profile_already_created_error import ProfileAlreadyCreatedError
from app.exception.profile_not_found_error import ProfileNotFoundError
from app.model.profile import Profile
from app.schema.profile_dto import ProfileDTO

from app.core.constants import constants

logger = logging.getLogger(__name__)

class ProfileService:
    def __init__(self, profile_crud: ProfileCRUD = Depends(ProfileCRUD),
                        rabbit_c: aio_pika.abc.AbstractChannel = Depends(rabbit_client)):
        self.profile_crud = profile_crud
        self.rabbit_c = rabbit_c

    async def create(self, profile: ProfileDTO, user_id: uuid.UUID, bg_tasks: BackgroundTasks):
        # if await self.profile_crud.check_if_profile_exists_by_user_id(user_id):
        #     profile_already_created_error = ProfileAlreadyCreatedError()
        #     logger.error(profile_already_created_error.message)
        #     raise profile_already_created_error
        #
        # await self.profile_crud.save(Profile(user_id=user_id,
        #                                      first_name=profile.first_name,
        #                                      last_name=profile.last_name,
        #                                      bio=profile.bio,
        #                                      latitude=profile.latitude,
        #                                      longitude=profile.longitude,
        #                                      age=profile.age,
        #                                      gender=profile.gender,
        #                                      phone_number=profile.phone_number))
        bg_tasks.add_task(self.rabbit_c.default_exchange.publish, aio_pika.Message(
                body=json.dumps({"id": str(user_id),
                                 "bio": profile.bio,
                                 "latitude":profile.latitude,
                                 "longitude":profile.longitude,
                    }).encode('utf-8')
                ), constants.PET_SUGGESTION_QUEUE_NAME
        )
        # await self.rabbit_c.default_exchange.publish(
        #     aio_pika.Message(
        #         body=json.dumps({"id": str(user_id),
        #                          "bio": profile.bio,
        #                          "latitude":profile.latitude,
        #                          "longitude":profile.longitude,
        # }).encode('utf-8')
        #     ),
        #     routing_key=constants.PET_SUGGESTION_QUEUE_NAME
        # )


    async def update(self, profile: ProfileDTO, user_id: uuid.UUID):
        await self.profile_crud.update(profile, user_id)

    async def get_profile(self, user_id: uuid.UUID) -> Profile:
        return await self.profile_crud.get_profile_by_user_id(user_id)