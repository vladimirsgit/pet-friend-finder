from fastapi import Depends, HTTPException, Security
import logging

from fastapi.security import APIKeyHeader
from jwt import PyJWTError

from starlette.status import HTTP_401_UNAUTHORIZED

from app.core.config import Config
from app.core.constants import constants
from app.exception.invalid_api_key_error import InvalidAPIKeyError

from app.exception.user_not_found_error import UserNotFoundError

from app.requests import users_mcrsrv

from app.schema.user_dto import UserDTO

from app.service.session_service import SessionService

from app.utils.oauth2 import oauth2_scheme

logger = logging.getLogger(__name__)

api_key_header = APIKeyHeader(name=constants.API_KEY_HEADER_NAME, auto_error=False)

async def get_logged_in_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = await SessionService.validate_access_token(token)
    except PyJWTError:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    username = payload.get('sub')
    if not username:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    try:
        user: UserDTO = await users_mcrsrv.read_user(username)
        if not user.confirmed:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    except UserNotFoundError:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    return user


async def check_internal_api_key(api_key: str = Security(api_key_header)):
    correct_api_key: str = Config.OWN_API_KEY
    if correct_api_key != api_key:
        raise InvalidAPIKeyError()