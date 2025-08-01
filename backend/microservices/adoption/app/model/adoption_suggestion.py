import uuid
from typing import List

from sqlalchemy import Column, UUID, ARRAY
from sqlmodel import SQLModel, Field

from app.enum.adoption_request_status import AdoptionRequestStatus

from datetime import datetime

class AdoptionSuggestion(SQLModel, table=True):
    __tablename__ = 'adoption_suggestion'
    __table_args__ = {"schema": "adoptions_svc"}

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(nullable=False, unique=True)
    suggestions: List[uuid.UUID] = Field(sa_column=Column(ARRAY(UUID)))