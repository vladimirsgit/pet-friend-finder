from fastapi.security import OAuth2PasswordBearer

from app.core.constants import constants

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{constants.AUTH_MICROSERVICE_URL}/login")