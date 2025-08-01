from fastapi import HTTPException

from starlette.status import HTTP_401_UNAUTHORIZED


class ProfileAlreadyCreatedError(HTTPException):
    def __init__(self, message="Profile already created."):
        super().__init__(status_code=HTTP_401_UNAUTHORIZED, detail=message)
        self.message = message