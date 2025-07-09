from typing import Optional

import redis.asyncio as redis
import logging

logger = logging.getLogger(__name__)

class RedisClient:
    client: Optional[redis.Redis] = None

    def __call__(self):
        return self.client

    async def init_redis(self):
        self.client = redis.Redis(host='redis')
        logger.info("Connected to redis")

    async def close_conn(self):
        await self.client.aclose()

redis_client = RedisClient()