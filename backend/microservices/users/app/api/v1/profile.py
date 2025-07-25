import logging

from fastapi import APIRouter, Security, Depends, HTTPException

from app.exception.profile_not_found_error import ProfileNotFoundError
from app.exception.user_not_found_error import UserNotFoundError

from app.requests.auth_mcrsrv import get_logged_in_user

from app.schema.profile_dto import ProfileDTO
from app.schema.user_dto import UserDTO
from app.service.profile_service import ProfileService

from app.service.user_service import UserService

from starlette.status import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/create")
async def create_profile(
        profile: ProfileDTO,
        profile_service: ProfileService = Depends(ProfileService),
        user: UserDTO = Depends(get_logged_in_user)
):
    await profile_service.create(profile, user.id)


@router.patch("/update")
async def update_profile(
        profile: ProfileDTO,
        profile_service: ProfileService = Depends(ProfileService),
        user: UserDTO = Depends(get_logged_in_user)
):
    try:
        await profile_service.update(profile, user.id)
    except ProfileNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=e.message)

@router.get("", response_model=ProfileDTO)
async def get_profile(
        profile_service: ProfileService = Depends(ProfileService),
        user: UserDTO = Depends(get_logged_in_user)
):
    try:
        return await profile_service.get_profile(user.id)
    except ProfileNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=e.message)