import logging
import uuid
from typing import Optional, List, Literal

from fastapi import APIRouter, Depends, HTTPException

from app.enum.gender import Gender
from app.enum.order import Order
from app.exception.pet_not_found_error import PetNotFoundError

from app.model.pet import Pet

from app.requests.auth_mcrsrv import get_logged_in_user

from app.schema.user_dto import UserDTO

from app.service.pet_service import PetService

from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/{pet_id}", response_model=Pet)
async def get_pet(
        pet_id: uuid.UUID,
        pet_service: PetService = Depends(PetService),
        user: UserDTO = Depends(get_logged_in_user),
):
    logger.info(f"Getting pet with id {pet_id} for user {user.username}")
    try:
        return await pet_service.get_pet_by_id(pet_id=pet_id)
    except PetNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=e.message)


@router.get("", response_model=List[Pet])
async def get_pets(
        name: Optional[str] = None,
        type: Optional[str] = None,
        breed: Optional[str] = None,
        age: Optional[int] = None,
        gender: Optional[Gender] = None,
        description: Optional[str] = None,
        vaccinated: Optional[bool] = None,
        owner_id: Optional[uuid.UUID] = None,
        sort: Literal["name", "type", "breed", "age"] = "name",
        order: Order = Order.asc,
        pet_service: PetService = Depends(PetService),
        user: UserDTO = Depends(get_logged_in_user),
):
    logger.info(f"Filtering pets by name {name}, type {type}, breed {breed}, age {age}, gender {gender}, description {description}, vaccinated {vaccinated}, owner_id {owner_id} and sorting by {sort} for user {user.username}")
    try:
        return await pet_service.filter_pets(name=name, type=type, breed=breed, age=age, gender=gender, description=description, vaccinated=vaccinated, owner_id=owner_id, sort=sort, order=order)
    except PetNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=e.message)
    except ValueError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))