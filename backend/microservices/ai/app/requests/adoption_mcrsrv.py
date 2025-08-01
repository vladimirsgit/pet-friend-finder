from typing import List, Optional

from httpx import HTTPStatusError

from app.core.constants import constants

import logging

import os

from fastapi import HTTPException, Depends, FastAPI

from starlette.status import HTTP_409_CONFLICT, HTTP_200_OK

import httpx

from app.schema.adoption_suggestion_dto import AdoptionSuggestionDTO
from app.schema.pet_desc_dto import PetDescDTO
from app.schema.user_dto import UserDTO
from app.utils.oauth2 import oauth2_scheme

logger = logging.getLogger(__name__)

async def get_animals_descriptions(latitude: Optional[float] = None, longitude: Optional[float] = None) -> List[PetDescDTO]:
    headers = {"x-api-key": os.getenv("ADOPTION_INTERNAL_SERVICE_API_KEY")}
    async with httpx.AsyncClient() as client:
        url = f"{constants.ADOPTION_MICROSERVICE_URL}/pets-desc"
        if True or (latitude and longitude):
            url += f"?latitude={latitude}&longitude={longitude}"
        response = await client.get(
            url=url,
            headers=headers
        )

    if response.status_code != HTTP_200_OK:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return [PetDescDTO(
        id=obj['id'],
        description=obj['description']
    ) for obj in response.json()]

async def save_suggestions(adoption_suggestion: AdoptionSuggestionDTO):
    headers = {"x-api-key": os.getenv("ADOPTION_INTERNAL_SERVICE_API_KEY")}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=f"{constants.ADOPTION_MICROSERVICE_URL}/suggestions",
                headers=headers,
                json=adoption_suggestion.model_dump(mode='json')
            )

        response.raise_for_status()
    except HTTPStatusError as e:
        logger.error(e)
