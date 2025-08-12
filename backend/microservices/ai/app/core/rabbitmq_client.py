import asyncio
from typing import Optional

import json

import aio_pika
import aio_pika.abc

import logging

from aiormq.exceptions import AMQPConnectionError

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