from app.core.constants import constants

import os

from fastapi import HTTPException

from starlette.status import HTTP_409_CONFLICT, HTTP_200_OK

import httpx

from app.schema.signup_request import SignUpRequest
from app.schema.signup_request_hashed_pass import SignUpRequestHashedPass
from app.schema.user_dto import UserDTO


async def check_if_user_exists(username: str) -> bool:
    headers = {"x-api-key": os.getenv("USERS_INTERNAL_SERVICE_API_KEY")}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{constants.USERS_MICROSERVICE_URL}/exists/{username}",
            headers=headers
        )

    return True if response.status_code == HTTP_409_CONFLICT else False


async def signup_user(signup_request: SignUpRequestHashedPass):
    headers = {"x-api-key": os.getenv("USERS_INTERNAL_SERVICE_API_KEY")}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{constants.USERS_MICROSERVICE_URL}/register",
            json=signup_request.model_dump(),
            headers=headers
        )
    if response.status_code != HTTP_200_OK:
        raise HTTPException(status_code=response.status_code, detail=response.text)


async def confirm_email(username: str):
    headers = {"x-api-key": os.getenv("USERS_INTERNAL_SERVICE_API_KEY")}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{constants.USERS_MICROSERVICE_URL}/confirm_email/{username}",
            headers=headers
        )
        response.raise_for_status()


async def read_user(username: str) -> UserDTO:
    headers = {"x-api-key": os.getenv("USERS_INTERNAL_SERVICE_API_KEY")}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{constants.USERS_MICROSERVICE_URL}/user/{username}",
            headers=headers
        )
        response.raise_for_status()
    json_resp = response.json()

    return UserDTO.model_validate(json_resp)
