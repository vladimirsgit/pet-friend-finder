import os
from typing import Optional

import redis.asyncio as redis
import logging

logger = logging.getLogger(__name__)

class RedisClient:
    client: Optional[redis.Redis] = None

    def __call__(self):
        return self.client

    async def init_redis(self):
        self.client = redis.Redis(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')), username=os.getenv('REDIS_USER'), password=os.getenv('REDIS_PASSWORD'), decode_responses=True)
        logger.info("Connected to redis")

    async def close_conn(self):
        await self.client.aclose()

redis_client = RedisClient()