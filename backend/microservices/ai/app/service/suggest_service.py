import uuid
from typing import List, Dict

from fastapi import HTTPException

from app.requests.adoption_mcrsrv import get_animals_descriptions, save_suggestions

import logging

from app.schema.adoption_suggestion_dto import AdoptionSuggestionDTO
from app.schema.pet_desc_dto import PetDescDTO

from transformers import pipeline

from app.schema.user_suggest_dto import UserSuggestDTO

logger = logging.getLogger(__name__)

class SuggestService:
    async def process_profile_created_suggestion(self, message_body: dict):
        logger.info("Starting to process suggestions based on desc...")


        user: UserSuggestDTO = UserSuggestDTO(**message_body)
        logger.info(f"USER_DATA_FOR_SUGGEST {user}")

        try:
            pets_desc: List[PetDescDTO] = await get_animals_descriptions(latitude=user.latitude, longitude=user.longitude)
        except HTTPException as e:
            logger.error(f"HTTP Exception while processing suggestions for: {user}")
            return
        logger.info(f"Retrieved pets desc {pets_desc}")

        pets_dict: Dict[str, uuid.UUID] = {pd.description: pd.id for pd in pets_desc}

        classifier = pipeline("zero-shot-classification",
                              model="facebook/bart-large-mnli")

        sequence_to_classify = user.bio

        classif_result = classifier(sequence_to_classify, list(pets_dict.keys()), multi_label=True)

        suggestions: List[uuid.UUID] = [pets_dict[label] for label in classif_result.get('labels')]
        logger.info(f"SUGGESTIONS, USER ID {suggestions}, {user.id}")

        await save_suggestions(AdoptionSuggestionDTO(user_id=user.id, suggestions=suggestions))