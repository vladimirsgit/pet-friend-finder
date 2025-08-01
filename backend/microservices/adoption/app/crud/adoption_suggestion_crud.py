import uuid

import logging

from typing import Optional, List

from app.crud.base_crud import BaseCRUD

from sqlmodel import select, and_

from app.enum.adoption_request_status import AdoptionRequestStatus
from app.exception.adoption_request_not_found_error import AdoptionRequestNotFoundError
from app.model.adoption_request import AdoptionRequest
from app.model.adoption_suggestion import AdoptionSuggestion

logger = logging.getLogger(__name__)

class AdoptionSuggestionCRUD(BaseCRUD):
    async def create(self, adoption_suggestion: AdoptionSuggestion):
        self.db.add(adoption_suggestion)
        await self.db.commit()

    async def check_if_exists(self, user_id: uuid.UUID) -> bool:
        stmt = select(1).where(AdoptionSuggestion.user_id == user_id)

        res = await self.db.execute(stmt)

        res = res.scalar_one_or_none()

        return bool(res)