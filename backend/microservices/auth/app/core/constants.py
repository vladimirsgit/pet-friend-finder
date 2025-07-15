from datetime import timedelta


class Constants:
    PASS_MAX_LEN = 32
    PASS_MIN_LEN = 1
    EMAIL_MAX_LEN = 320

    REFRESH_TOKEN_REDIS_KEY = "REFRESH_TOKEN"

    REFRESH_TOKEN_EXP = timedelta(minutes=60)
    ACCESS_TOKEN_EXP = timedelta(minutes=0)

    EMAIL_VALIDATION_CODE_EXP = timedelta(minutes=5)
    PASSWORD_CHANGE_TOKEN_EXP = timedelta(minutes=5)

    USERS_MICROSERVICE_URL = "http://users-microservice:8001/api/v1/internal"

constants = Constants()