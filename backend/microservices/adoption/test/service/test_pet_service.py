import os
os.environ["DATABASE_HOST"] = "test"
os.environ["DATABASE_PORT"] = "0000"
os.environ["POSTGRES_USER"] = "test"
os.environ["POSTGRES_PASSWORD"] = "test"
os.environ["POSTGRES_DB"] = "test"

import uuid
import pytest
from unittest.mock import AsyncMock
from app.model.pet import Pet
from app.service.pet_service import PetService

@pytest.mark.asyncio
async def test_get_pet_by_id():
    pet_id = uuid.uuid4()

    mock_pet_crud = AsyncMock()
    mock_pet_crud.get_pet_by_id.return_value = Pet(id=pet_id, **{})

    pet = await PetService(pet_crud=mock_pet_crud).get_pet_by_id(pet_id)

    mock_pet_crud.get_pet_by_id.assert_awaited_once_with(pet_id)

    assert pet.id == pet_id
