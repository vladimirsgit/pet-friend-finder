import logging

from fastapi import APIRouter, BackgroundTasks, Depends

from app.schema.signup_request import SignUpRequest
from service.auth_service import AuthService

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/signup")
async def signup(
        signup_request: SignUpRequest,
        auth_service: AuthService = Depends(AuthService),
):
    logger.info(f"Processing signup request...")


