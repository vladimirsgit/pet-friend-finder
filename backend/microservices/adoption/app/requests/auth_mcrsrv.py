from app.core.constants import constants

import os

from fastapi import HTTPException, Depends

from starlette.status import HTTP_409_CONFLICT, HTTP_200_OK

import httpx


from app.schema.user_dto import UserDTO
from app.utils.oauth2 import oauth2_scheme


async def get_logged_in_user(token: str = Depends(oauth2_scheme)) -> UserDTO:
    headers = {"x-api-key": os.getenv("AUTH_INTERNAL_SERVICE_API_KEY"),
               "Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{constants.AUTH_MICROSERVICE_URL}/logged-user",
            headers=headers
        )
    if response.status_code != HTTP_200_OK:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return UserDTO.model_validate(response.json())