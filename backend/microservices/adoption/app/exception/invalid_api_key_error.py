from fastapi import HTTPException

from starlette.status import HTTP_401_UNAUTHORIZED


class InvalidAPIKeyError(HTTPException):
    def __init__(self, message="Invalid API key."):
        super().__init__(status_code=HTTP_401_UNAUTHORIZED, detail=message)
        self.message = message