from fastapi import Depends, HTTPException
import logging

from jwt import PyJWTError

from starlette.status import HTTP_401_UNAUTHORIZED

from app.exceptions.user_not_found_error import UserNotFoundError

from app.requests import users_mcrsrv

from app.schema.user_dto import UserDTO

from app.service.session_service import SessionService

from app.utils.oauth2 import oauth2_scheme

logger = logging.getLogger(__name__)

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