import logging

from fastapi import APIRouter, Security, Depends, HTTPException

from app.exception.user_not_found_error import UserNotFoundError

from app.requests.auth_mcrsrv import get_logged_in_user

from app.schema.profile_dto import ProfileDTO
from app.schema.user_dto import UserDTO
from app.service.profile_service import ProfileService

from app.service.user_service import UserService

from starlette.status import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/create")
async def create_profile(
        profile: ProfileDTO,
        profile_service: ProfileService = Depends(ProfileService),
        user: UserDTO = Depends(get_logged_in_user)
):
    await profile_service.save(profile)

