import logging

from fastapi import APIRouter, Security, Depends, HTTPException

from app.exceptions.user_not_found_error import UserNotFoundError
from app.schema.signup_request import SignUpRequest
from app.core.dependencies import check_internal_api_key
from app.service.user_service import UserService

from starlette.status import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/register")
async def register(
        signup_request: SignUpRequest,
        api_key: str = Security(check_internal_api_key),
        user_service: UserService = Depends(UserService),
):
    logger.info(f"Processing signup request...")
    try:
        await user_service.signup(signup_request)
    except ValueError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/exists/{username}")
async def check_if_username_exists(
        username: str,
        api_key: str = Security(check_internal_api_key),
        user_service: UserService = Depends(UserService),
):
    logger.info(f"Getting user {username}...")
    if await user_service.check_if_username_exists(username):
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail="Username already exists.")


@router.get("/confirm_email/{username}")
async def confirm_email(
        username: str,
        api_key: str = Security(check_internal_api_key),
        user_service: UserService = Depends(UserService),
):
    logger.info(f"Confirming email for user with username {username}...")
    try:
        await user_service.confirm_email(username)
    except UserNotFoundError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))