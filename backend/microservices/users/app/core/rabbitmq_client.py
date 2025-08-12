from typing import Optional

import aio_pika
import aio_pika.abc

from aiormq.exceptions import AMQPConnectionError

import asyncio

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

        for attempt in range(10):
            try:
                self.connection = await aio_pika.connect_robust(url)
                break
            except AMQPConnectionError as e:
                error_message = str(e) + f"Failed to connect to rabbitmq client, attempt #{attempt + 1}."
                if attempt < 9:
                    error_message += " Retrying..."
                logger.error(error_message)
                if attempt < 9:
                    await asyncio.sleep(10)

        self.channel = await self.connection.channel()
        await self.channel.declare_queue(name=constants.PET_SUGGESTION_QUEUE_NAME, durable=True)

        logger.info("Connected to rabbitmq")

    async def close_conn(self):
        await self.connection.close()

rabbit_client = RabbitMQClient()