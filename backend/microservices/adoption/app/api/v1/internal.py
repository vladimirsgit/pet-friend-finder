import logging
from typing import List, Optional

from fastapi import APIRouter, Security, Depends, HTTPException

from app.core.dependencies import check_internal_api_key


from starlette.status import HTTP_400_BAD_REQUEST

from app.exception.adoption_suggestion_exists_error import AdoptionSuggestionExistsError
from app.model.adoption_suggestion import AdoptionSuggestion
from app.schema.adoption_suggestion_dto import AdoptionSuggestionDTO
from app.schema.pet_desc_dto import PetDescDTO
from app.service.adoption_suggestion_service import AdoptionSuggestionService
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


@router.post("/suggestions")
async def add_suggestions(
        adoption_suggestions: AdoptionSuggestionDTO,
        adoption_suggestion_service: AdoptionSuggestionService = Depends(AdoptionSuggestionService),
        api_key: str = Security(check_internal_api_key)
):
    logger.info(f"Adding suggested pets...")
    try:
        await adoption_suggestion_service.create(AdoptionSuggestion(**adoption_suggestions.model_dump()))
    except AdoptionSuggestionExistsError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=e.message)