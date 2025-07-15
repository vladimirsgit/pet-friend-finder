import redis.asyncio as redis
from fastapi import Depends

from app.schema.signup_request import SignUpRequest

import app.requests.users_mcrsrv as users_mcrsrv

from app.core.constants import constants
from app.core.redis_client import redis_client
from app.schema.signup_request_hashed_pass import SignUpRequestHashedPass

from app.utils.cryptos import get_email_confirmation_code, hash_with_hashlib, hash_with_bcrypt

import httpx

import os

class AuthService:
    def __init__(self, r_client: redis.Redis = Depends(redis_client)):
        self.r_client = r_client

    async def signup(self, signup_request: SignUpRequest):
        password, confirm_password = signup_request.password, signup_request.confirm_password
        await self.__validate_signup_password(password, confirm_password)

        if await users_mcrsrv.check_if_user_exists(signup_request.username):
            raise ValueError('Username already exists.')

        verification_code = await get_email_confirmation_code()
        hashed_code = await hash_with_hashlib(verification_code)
        code_exists: bool = bool(await self.r_client.get(hashed_code))

        while code_exists:
            verification_code = await get_email_confirmation_code()
            hashed_code = await hash_with_hashlib(verification_code)
            code_exists: bool = bool(await self.r_client.get(hashed_code))

        await users_mcrsrv.signup_user(SignUpRequestHashedPass(email=signup_request.email, username=signup_request.username, hashed_password=hash_with_bcrypt(signup_request.password)))


    async def __validate_signup_password(self, password, confirm_password):
        if password != confirm_password:
            raise ValueError('Passwords do not match')
        if len(password) < constants.PASS_MIN_LEN or len(password) > constants.PASS_MAX_LEN:
            raise ValueError(
                f'Password must be at least {constants.PASS_MIN_LEN} characters and at most {constants.PASS_MAX_LEN} characters.')