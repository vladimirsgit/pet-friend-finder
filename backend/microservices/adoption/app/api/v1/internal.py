import logging
from typing import List, Optional

from fastapi import APIRouter, Security, Depends, HTTPException

from app.core.dependencies import check_internal_api_key


from starlette.status import HTTP_400_BAD_REQUEST

from app.schema.pet_desc_dto import PetDescDTO
from app.service.pet_service import PetService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/pets-desc", response_model=List[PetDescDTO])
async def get_all_pets_desc(
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        pets_service: PetService = Depends(PetService),
        api_key: str = Security(check_internal_api_key)
):
    logger.info(f"Getting pets with descriptions...")
    return await pets_service.get_pets_with_descriptions(latitude=latitude, longitude=longitude)

