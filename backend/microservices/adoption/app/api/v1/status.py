import logging
from fastapi import APIRouter

router = APIRouter()

logger = logging.getLogger(__name__)
@router.get("", response_model=str)
async def check_status():
    logger.info("Checking server status...")
    return "Adoption microservice up and running"