from app.crud.base_crud import BaseCRUD
from app.schema.user_register_dto import User


class UserCRUD(BaseCRUD):
    async def save(self, user: User):
        self.db.add(user)