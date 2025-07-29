import logging
import uuid
from typing import Optional, List, Literal

from fastapi import APIRouter, Depends, HTTPException

from app.enum.adoption_request_status import AdoptionRequestStatus
from app.exception.adoption_request_exists_error import AdoptionRequestExistsError
from app.exception.adoption_request_not_found_error import AdoptionRequestNotFoundError
from app.exception.invalid_adoption_action_error import InvalidAdoptionActionError
from app.exception.pet_not_found_error import PetNotFoundError
from app.model.adoption_request import AdoptionRequest

from app.requests.auth_mcrsrv import get_logged_in_user

from app.schema.user_dto import UserDTO
from app.service.adoption_request_service import AdoptionRequestService

from app.core.constants import constants

from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/{pet_id}")
async def request_adoption(
        pet_id: uuid.UUID,
        adoption_request_service: AdoptionRequestService = Depends(AdoptionRequestService),
        user: UserDTO = Depends(get_logged_in_user),
):
    logger.info(f"Sending adoption request for pet {pet_id} by user {user.username}")
    try:
        await adoption_request_service.create_request(pet_id=pet_id, requester_id=user.id)
    except PetNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=e.message)
    except (AdoptionRequestExistsError, ValueError) as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/received-requests", response_model=List[AdoptionRequest])
async def get_received_adoption_requests(
        status: Optional[AdoptionRequestStatus] = None,
        adoption_request_service: AdoptionRequestService = Depends(AdoptionRequestService),
        user: UserDTO = Depends(get_logged_in_user)
):
    logger.info(f"Getting received adoption requests with status {status} for user {user.username}")
    return await adoption_request_service.get_received_adoption_requests(user_id=user.id, status=status)

@router.get("/sent-requests", response_model=List[AdoptionRequest])
async def get_sent_adoption_requests(
        status: Optional[AdoptionRequestStatus] = None,
        adoption_request_service: AdoptionRequestService = Depends(AdoptionRequestService),
        user: UserDTO = Depends(get_logged_in_user)
):
    logger.info(f"Getting sent adoption requests with status {status} for user {user.username}")
    return await adoption_request_service.get_sent_adoption_requests(user_id=user.id, status=status)


@router.patch("/requests/{action}")
async def perform_adoption_action(
        pet_id: uuid.UUID,
        requester_id: uuid.UUID,
        action: Literal["ACCEPT", "REJECT", "WITHDRAW"],
        adoption_request_service: AdoptionRequestService = Depends(AdoptionRequestService),
        user: UserDTO = Depends(get_logged_in_user),
):
    logger.info(f"Performing action {action} on adoption request with pet_id {pet_id} by user {user.username}")
    try:
        await adoption_request_service.handle_adoption_action(action=action, pet_id=pet_id, user=user, requester_id=requester_id)
    except AdoptionRequestNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=e.message)
    except InvalidAdoptionActionError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=e.message)