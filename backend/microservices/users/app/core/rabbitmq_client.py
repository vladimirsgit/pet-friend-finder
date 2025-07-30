from typing import Optional

import aio_pika
import aio_pika.abc

import logging

from app.core.constants import constants

import os

logger = logging.getLogger(__name__)

class RabbitMQClient:
    connection: Optional[aio_pika.abc.AbstractRobustConnection] = None
    channel: Optional[aio_pika.abc.AbstractChannel] = None

    def __call__(self):
        return self.channel

    async def init_rabbit(self):
        url = f"amqp://{os.getenv('RABBIT_USERNAME')}:{os.getenv('RABBIT_PASSWORD')}@{os.getenv('RABBIT_HOST')}:{os.getenv('RABBIT_PORT')}/"
        self.connection = await aio_pika.connect_robust(url)

        self.channel = await self.connection.channel()
        await self.channel.declare_queue(name=constants.PET_SUGGESTION_QUEUE_NAME, durable=True)

        logger.info("Connected to rabbitmq")

    async def close_conn(self):
        await self.connection.close()

rabbit_client = RabbitMQClient()