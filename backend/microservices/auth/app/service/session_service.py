import secrets

import jwt

import uuid
import logging
from datetime import datetime, timedelta
import redis.asyncio as redis

from fastapi import Depends

from app.core.redis_client import redis_client
from app.core.config import Config

from app.exception.refresh_token_expired_error import RefreshTokenExpiredError

from app.schema.access_token import AccessToken
from app.schema.authorization_tokens import AuthorizationTokens
from app.schema.refresh_token import RefreshToken

from app.utils.cryptos import hash_with_hashlib

from app.core.constants import constants

logger = logging.getLogger(__name__)

class SessionService:
    def __init__(self, r_client: redis.Redis = Depends(redis_client)):
        self.r_client = r_client


    @staticmethod
    async def generate_access_token(username: str) -> AccessToken:
        payload = {
            "sub": username,
            "exp": datetime.now() + constants.ACCESS_TOKEN_EXP
        }
        return AccessToken(token=jwt.encode(payload, Config.SECRET_KEY, Config.ALGORITHM))

    @staticmethod
    async def generate_refresh_token() -> RefreshToken:
        return RefreshToken(token=secrets.token_urlsafe(32))


    @staticmethod
    async def generate_tokens_after_login(username: str)-> AuthorizationTokens:
        access_token: AccessToken = await SessionService.generate_access_token(username)
        refresh_token: RefreshToken = await SessionService.generate_refresh_token()

        return AuthorizationTokens(access_token=access_token, refresh_token=refresh_token)


    @staticmethod
    async def validate_access_token(token: str):
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        return payload


    async def validate_refresh_token(self, refresh_token: str) -> AuthorizationTokens:
        hashed_token = await hash_with_hashlib(refresh_token)
        username = await self.r_client.get(hashed_token)
        if not username:
            error = RefreshTokenExpiredError()
            logger.error(error.message)
            raise error
        username = username.decode('utf-8')

        new_refresh_token = await SessionService.generate_refresh_token()
        await self.r_client.delete(hashed_token)
        hashed_new_refresh_token = await hash_with_hashlib(new_refresh_token.token)

        await self.r_client.set(name=hashed_new_refresh_token, value=username,  ex=int(constants.REFRESH_TOKEN_EXP.total_seconds()))

        new_access_token = await SessionService.generate_access_token(username)

        return AuthorizationTokens(access_token=new_access_token, refresh_token=new_refresh_token)



