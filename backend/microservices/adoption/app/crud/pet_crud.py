import uuid

import logging

from typing import Optional, List

from app.crud.base_crud import BaseCRUD
from app.enum.gender import Gender
from app.enum.order import Order
from app.exception.pet_not_found_error import PetNotFoundError
from app.model.pet import Pet

from sqlmodel import select, and_

from sqlalchemy import func

from app.schema.pet_desc_dto import PetDescDTO

logger = logging.getLogger(__name__)

class PetCRUD(BaseCRUD):
    async def get_pet_by_id(self, pet_id: uuid.UUID) -> Pet:
        stmt = select(Pet).where(Pet.id == pet_id)
        res = await self.db.execute(stmt)

        pet: Optional[Pet] = res.scalar_one_or_none()

        if not pet:
            pet_not_found_error = PetNotFoundError()
            logger.error(pet_not_found_error.message)
            raise pet_not_found_error

        return pet

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
        stmt = select(Pet)
        if name:
            stmt = stmt.where(Pet.name.ilike(f"%{name}%"))
        if type:
            stmt = stmt.where(Pet.type.ilike(f"%{type}%"))
        if breed:
            stmt = stmt.where(Pet.breed.ilike(f"%{breed}%"))
        if age:
            stmt = stmt.where(Pet.age == age)
        if gender:
            stmt = stmt.where(Pet.gender == gender)
        if description:
            stmt = stmt.where(Pet.description.ilike(f"%{description}%"))
        if vaccinated:
            stmt = stmt.where(Pet.vaccinated == vaccinated)
        if owner_id:
            stmt = stmt.where(Pet.owner_id == owner_id)

        if order == Order.desc:
            stmt = stmt.order_by(getattr(Pet, sort).desc())
        else:
            stmt = stmt.order_by(getattr(Pet, sort))

        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def get_pets_with_descriptions(self, latitude: Optional[float] = None, longitude: Optional[float] = None) -> List[PetDescDTO]:
        stmt = select(Pet.id, Pet.description)

        if latitude and longitude:
            stmt = stmt.where(and_(func.abs(Pet.latitude - latitude) <= 1), func.abs(Pet.longitude - longitude) <= 1)

        res = await self.db.execute(stmt)

        return [PetDescDTO(
            id=res_obj[0],
            description=res_obj[1]
        ) for res_obj in res.all()]

    async def add_pet(self, pet: Pet):
        self.db.add(pet)
        await self.db.commit()