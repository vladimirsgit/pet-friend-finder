import logging

from fastapi import APIRouter, Security, Depends
from app.core.dependencies import check_internal_api_key
from app.schema.user_dto import UserDTO


from app.core.dependencies import get_logged_in_user


router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/logged-user", response_model=UserDTO)
async def get_logged_in_user(
        api_key: str = Security(check_internal_api_key),
        user: UserDTO = Depends(get_logged_in_user)
):
    return user