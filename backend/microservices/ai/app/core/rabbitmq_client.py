from typing import Optional

import json

import aio_pika
import aio_pika.abc

import logging

from app.core.constants import constants

from app.service.suggest_service import SuggestService

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

        async with self.connection:
            self.channel = await self.connection.channel()
            queue: aio_pika.abc.AbstractQueue = await self.channel.declare_queue(name=constants.PET_SUGGESTION_QUEUE_NAME, durable=True)
            #
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        logger.info("Processing message from rabbitmq...")
                        await SuggestService().process_profile_created_suggestion(json.loads(message.body.decode()))

        logger.info("Connected to rabbitmq")

    async def close_conn(self):
        await self.connection.close()

rabbit_client = RabbitMQClient()