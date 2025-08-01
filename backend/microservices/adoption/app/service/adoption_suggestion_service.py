import logging

from fastapi import Depends

from app.crud.adoption_suggestion_crud import AdoptionSuggestionCRUD
from app.exception.adoption_suggestion_exists_error import AdoptionSuggestionExistsError
from app.model.adoption_suggestion import AdoptionSuggestion


logger = logging.getLogger(__name__)

class AdoptionSuggestionService:
    def __init__(self, adoption_suggestion_crud: AdoptionSuggestionCRUD = Depends(AdoptionSuggestionCRUD)):
        self.adoption_suggestion_crud = adoption_suggestion_crud

    async def create(self, adoption_suggestion: AdoptionSuggestion):
        exists: bool = await self.adoption_suggestion_crud.check_if_exists(adoption_suggestion.user_id)

        if exists:
            adoption_suggestion_exists_error = AdoptionSuggestionExistsError()
            logger.error(adoption_suggestion_exists_error.message)
            raise adoption_suggestion_exists_error

        await self.adoption_suggestion_crud.create(adoption_suggestion)
