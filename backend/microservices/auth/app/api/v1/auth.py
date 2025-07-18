import logging

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from httpx import HTTPStatusError

from app.exceptions.invalid_code_error import InvalidCodeError
from app.exceptions.invalid_credentials_error import InvalidCredentialsError
from app.schema.authorization_tokens import AuthorizationTokens
from app.schema.login_request import LogInRequest
from app.schema.signup_request import SignUpRequest

from starlette.status import HTTP_409_CONFLICT, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from app.service.auth_service import AuthService

from app.utils.mailer import send_verification_mail

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/signup")
async def signup(
        signup_request: SignUpRequest,
        bg_tasks: BackgroundTasks,
        auth_service: AuthService = Depends(AuthService)
):
    logger.info(f"Processing signup request...")

    try:
        verification_code = await auth_service.signup(signup_request)
        bg_tasks.add_task(send_verification_mail, signup_request.email, signup_request.username, verification_code)
    except ValueError as e:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(e))

@router.get("/confirm_email/{code}")
async def confirm_email(
        code: str,
        auth_service: AuthService = Depends(AuthService)
):
    logger.info(f"Processing email confirmation request...")
    try:
        await auth_service.confirm_email(code)
    except InvalidCodeError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=AuthorizationTokens)
async def login(
        login_request: LogInRequest,
        auth_service: AuthService = Depends(AuthService),
):
    try:
        logger.info(f'Processing log in request for {login_request.username}...')
        return await auth_service.login(login_request)
    except (InvalidCredentialsError, HTTPStatusError):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
