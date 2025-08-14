from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter, Request, Depends
from starlette.responses import JSONResponse
from app.core.db import init_db
from app.core.redis_client import redis_client
from app.core.rabbitmq_client import rabbit_client
import logging

from app.api.v1 import internal, profile

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s: %(levelname)s: %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    logger.info("Connected to db")
    await redis_client.init_redis()
    await rabbit_client.init_rabbit()
    yield
    await redis_client.close_conn()
    await rabbit_client.close_conn()


app = FastAPI(lifespan=lifespan)

api_router = APIRouter(prefix="/api/v1/users")
api_router.include_router(internal.router, prefix="/internal", tags=["internal"])
api_router.include_router(profile.router, prefix="/profile", tags=["profile"])
app.include_router(api_router)

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(exc)
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred. Please try again."},
    )
