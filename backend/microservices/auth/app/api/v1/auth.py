import logging

from fastapi import APIRouter, BackgroundTasks, Depends

from app.schema.signup_request import SignUpRequest

from app.service.auth_service import AuthService

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/signup")
async def register(
        signup_request: SignUpRequest,
        auth_service: AuthService = Depends(AuthService),
):
    logger.info(f"Processing signup request...")

    return await auth_service.register(signup_request)
