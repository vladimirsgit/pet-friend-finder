import logging

from fastapi import APIRouter, Security

from app.schema.signup_request import SignUpRequest
from app.core.dependencies import check_internal_api_key

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/register")
async def register(
        signup_request: SignUpRequest,
        api_key: str = Security(check_internal_api_key)
):
    logger.info(f"Processing signup request...")
    print(signup_request)

