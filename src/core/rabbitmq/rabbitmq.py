from typing import Any, Optional

from aio_pika import DeliveryMode, Message, connect
from aio_pika.abc import AbstractConnection

from src.core.settings import settings

mq_connect: Optional[AbstractConnection] = None


class RabbitMQ:

    """
    Singleton class for working with RabbitMQ
    """

    __instance: Optional[Any] = None
    __mq_connect: Optional[AbstractConnection] = None

    @classmethod
    async def connect(cls):
        cls.__mq_connect = await connect(
            f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASS}@{settings.RABBITMQ_HOST}/"
        )

    @classmethod
    async def close(cls):
        if cls.__mq_connect:
            await cls.__mq_connect.close()

    @classmethod
    async def send_message(cls, queue_name: str, message_body: str):
        if cls.__mq_connect:
            async with cls.__mq_connect.channel() as mq_channel:
                message = Message(
                    body=message_body.encode("utf-8"),
                    delivery_mode=DeliveryMode.PERSISTENT,
                )
                await mq_channel.default_exchange.publish(
                    message=message,
                    routing_key=queue_name,
                )

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(RabbitMQ, cls).__new__(cls)
        return cls.__instance

