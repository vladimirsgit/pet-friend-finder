import logging

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from app.schema.signup_request import SignUpRequest

from starlette.status import HTTP_409_CONFLICT

from app.service.auth_service import AuthService

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/signup")
async def signup(
        signup_request: SignUpRequest,
        auth_service: AuthService = Depends(AuthService),
):
    logger.info(f"Processing signup request...")

    try:
        return await auth_service.signup(signup_request)
    except ValueError as e:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(e))