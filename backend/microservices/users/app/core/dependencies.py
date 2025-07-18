import os

from fastapi import Security

from app.core.constants import constants
from app.core.config import Config

from fastapi.security import APIKeyHeader

from app.exceptions.invalid_api_key_error import InvalidAPIKeyError

api_key_header = APIKeyHeader(name=constants.API_KEY_HEADER_NAME, auto_error=False)

async def check_internal_api_key(api_key: str = Security(api_key_header)):
    correct_api_key: str = Config.OWN_API_KEY
    if correct_api_key != api_key:
        raise InvalidAPIKeyError()