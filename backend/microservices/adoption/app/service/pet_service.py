import uuid
from typing import List, Optional

from fastapi import Depends

from app.crud.pet_crud import PetCRUD
from app.enum.gender import Gender
from app.enum.order import Order
from app.model.pet import Pet
from app.schema.pet_create_dto import PetCreate
from app.schema.pet_desc_dto import PetDescDTO


class PetService:
    def __init__(self, pet_crud: PetCRUD = Depends(PetCRUD)):
        self.pet_crud = pet_crud

    async def get_pet_by_id(self, pet_id: uuid.UUID) -> Pet:
        return await self.pet_crud.get_pet_by_id(pet_id)

    async def filter_pets(self, name: Optional[str] = None,
                          type: Optional[str] = None,
                          breed: Optional[str] = None,
                          age: Optional[int] = None,
                          gender: Optional[Gender] = None,
                          description: Optional[str] = None,
                          vaccinated: Optional[bool] = None,
                          owner_id: Optional[uuid.UUID] = None,
                          sort: str = "name",
                          order: Order = Order.asc) -> List[Pet]:
        if sort not in Pet.model_fields.keys():
            raise ValueError(f"Sort by {sort} not supported.")
        return await self.pet_crud.filter_pets(name=name, type=type, breed=breed, age=age, gender=gender, description=description, vaccinated=vaccinated, owner_id=owner_id, sort=sort, order=order)

    async def get_pets_with_descriptions(self, latitude: Optional[float] = None, longitude: Optional[float] = None) -> List[PetDescDTO]:
        return await self.pet_crud.get_pets_with_descriptions(latitude, longitude)

    async def add_pet(self, pet: Pet, user_id: uuid.UUID):
        pet.owner_id = user_id
        await self.pet_crud.add_pet(pet)
