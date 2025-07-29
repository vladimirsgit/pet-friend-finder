import uuid

import logging

from typing import Optional, List

from app.crud.base_crud import BaseCRUD

from sqlmodel import select, and_

from app.enum.adoption_request_status import AdoptionRequestStatus
from app.exception.adoption_request_not_found_error import AdoptionRequestNotFoundError
from app.model.adoption_request import AdoptionRequest

logger = logging.getLogger(__name__)

class AdoptionRequestCRUD(BaseCRUD):
    async def check_if_exists(self, adoption_request: AdoptionRequest) -> bool:
        stmt = select(AdoptionRequest).where(and_(AdoptionRequest.requester_id == adoption_request.requester_id),
                                                    AdoptionRequest.pet_id == adoption_request.pet_id)
        res = await self.db.execute(stmt)

        return True if res.scalar_one_or_none() else False

    async def get_adoption_request(self,  pet_id: uuid.UUID, requester_id: uuid.UUID) -> AdoptionRequest:
        stmt = select(AdoptionRequest).where(and_(AdoptionRequest.requester_id == requester_id),
                                                    AdoptionRequest.pet_id == pet_id)
        res = await self.db.execute(stmt)
        res = res.scalar_one_or_none()

        if not res:
            adoption_request_not_found_error = AdoptionRequestNotFoundError()
            logger.error(adoption_request_not_found_error.message)
            raise adoption_request_not_found_error

        return res

    async def get_received_adoption_requests(self, user_id: uuid.UUID, status: Optional[AdoptionRequestStatus] = None) -> List[AdoptionRequest]:
        stmt = select(AdoptionRequest).where(AdoptionRequest.owner_id == user_id)

        if status:
            stmt = stmt.where(AdoptionRequest.status == status)

        res = await self.db.execute(stmt)

        return list(res.scalars().all())

    async def get_sent_adoption_requests(self, user_id: uuid.UUID, status: Optional[AdoptionRequestStatus] = None) -> List[AdoptionRequest]:
        stmt = select(AdoptionRequest).where(AdoptionRequest.requester_id == user_id)

        if status:
            stmt = stmt.where(AdoptionRequest.status == status)

        res = await self.db.execute(stmt)

        return list(res.scalars().all())

    async def create_request(self, adoption_request: AdoptionRequest):
        self.db.add(adoption_request)
        await self.db.commit()

    async def update_adoption_request(self, adoption_request: AdoptionRequest):
        self.db.add(adoption_request)
        await self.db.commit()