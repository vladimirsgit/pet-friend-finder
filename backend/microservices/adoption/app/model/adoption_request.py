import uuid

from sqlmodel import SQLModel, Field

from app.enum.adoption_request_status import AdoptionRequestStatus

from datetime import datetime

class AdoptionRequest(SQLModel, table=True):
    __tablename__ = 'adoption_request'
    __table_args__ = {"schema": "adoptions_svc"}

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    requester_id: uuid.UUID = Field(nullable=False)
    pet_id: uuid.UUID = Field(nullable=False)
    owner_id: uuid.UUID = Field(nullable=False)
    status: AdoptionRequestStatus = Field(nullable=False, default=AdoptionRequestStatus.PENDING)
    created_at: datetime = Field(nullable=False, default_factory=datetime.now)
    modified_at: datetime = Field(nullable=False, default_factory=datetime.now)