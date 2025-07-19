from datetime import timedelta


class Constants:
    PASS_MAX_LEN = 32
    PASS_MIN_LEN = 4
    EMAIL_MAX_LEN = 320
    USERNAME_MAX_LEN = 32

    REFRESH_TOKEN_REDIS_KEY = "REFRESH_TOKEN"

    REFRESH_TOKEN_EXP = timedelta(minutes=60)
    ACCESS_TOKEN_EXP = timedelta(minutes=0)

    EMAIL_VALIDATION_CODE_EXP = timedelta(minutes=5)
    PASSWORD_CHANGE_TOKEN_EXP = timedelta(minutes=5)

    AUTH_MICROSERVICE_URL = "http://auth-microservice:8002/api/v1/internal"

    API_KEY_HEADER_NAME = "x-api-key"

constants = Constants()