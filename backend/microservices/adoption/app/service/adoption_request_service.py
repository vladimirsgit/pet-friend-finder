import uuid

import logging
from typing import List, Optional

from fastapi import Depends

from app.crud.adoption_request_crud import AdoptionRequestCRUD
from app.enum.adoption_request_status import AdoptionRequestStatus
from app.exception.adoption_request_exists_error import AdoptionRequestExistsError
from app.exception.invalid_adoption_action_error import InvalidAdoptionActionError
from app.model.adoption_request import AdoptionRequest
from app.model.pet import Pet
from app.schema.user_dto import UserDTO
from app.service.pet_service import PetService

from app.core.constants import constants

logger = logging.getLogger(__name__)

class AdoptionRequestService:
    def __init__(self, adoption_request_crud: AdoptionRequestCRUD = Depends(AdoptionRequestCRUD),
                        pet_service: PetService = Depends(PetService)):
        self.adoption_request_crud = adoption_request_crud
        self.pet_service = pet_service

    async def check_if_exists(self, adoption_request: AdoptionRequest) -> bool:
        return await self.adoption_request_crud.check_if_exists(adoption_request)

    async def get_adoption_request(self, pet_id: uuid.UUID, requester_id: uuid.UUID) -> AdoptionRequest:
        return await self.adoption_request_crud.get_adoption_request(pet_id=pet_id, requester_id=requester_id)

    async def get_received_adoption_requests(self, user_id: uuid.UUID, status: Optional[AdoptionRequestStatus] = None) -> List[AdoptionRequest]:
        return await self.adoption_request_crud.get_received_adoption_requests(user_id, status=status)

    async def get_sent_adoption_requests(self, user_id: uuid.UUID, status: Optional[AdoptionRequestStatus] = None) -> List[AdoptionRequest]:
        return await self.adoption_request_crud.get_sent_adoption_requests(user_id=user_id, status=status)

    async def create_request(self, requester_id: uuid.UUID, pet_id: uuid.UUID):
        # raises pet not found if necessary
        pet: Pet = await self.pet_service.get_pet_by_id(pet_id)
        if pet.owner_id == requester_id:
            raise ValueError("Cannot adopt your own pet.")

        adoption_request: AdoptionRequest = AdoptionRequest(requester_id=requester_id, pet_id=pet_id, owner_id=pet.owner_id)

        if await self.check_if_exists(adoption_request):
            adoption_request_exists_error = AdoptionRequestExistsError()
            logger.error(adoption_request_exists_error.message)
            raise adoption_request_exists_error

        await self.adoption_request_crud.create_request(adoption_request)

    async def handle_adoption_action(self, action: str, pet_id: uuid.UUID, user: UserDTO, requester_id: uuid.UUID):
        if action == "WITHDRAW":
            await self.__handle_withdraw_adoption_action(pet_id, user)
        else:
            await self.__handle_accept_reject_adoption_action(action, pet_id, user, requester_id)

    async def __handle_withdraw_adoption_action(self, pet_id: uuid.UUID, user: UserDTO):
        adoption_request: AdoptionRequest = await self.get_adoption_request(pet_id=pet_id, requester_id=user.id)

        if adoption_request.status != AdoptionRequestStatus.PENDING:
            invalid_adoption_action_error = InvalidAdoptionActionError()
            logger.error(invalid_adoption_action_error.message)
            raise invalid_adoption_action_error

        adoption_request.status = AdoptionRequestStatus.WITHDREW

        await self.adoption_request_crud.update_adoption_request(adoption_request)

    async def __handle_accept_reject_adoption_action(self, action: str, pet_id: uuid.UUID, user: UserDTO, requester_id: uuid.UUID):
        adoption_request: AdoptionRequest = await self.get_adoption_request(pet_id=pet_id, requester_id=requester_id)

        if adoption_request.status != AdoptionRequestStatus.PENDING or user.id == requester_id or user.id != adoption_request.owner_id:
            invalid_adoption_action_error = InvalidAdoptionActionError()
            logger.error(invalid_adoption_action_error.message)
            raise invalid_adoption_action_error

        if action == "ACCEPT":
            adoption_request.status = AdoptionRequestStatus.ACCEPTED
        else:
            adoption_request.status = AdoptionRequestStatus.REJECTED

        await self.adoption_request_crud.update_adoption_request(adoption_request)
