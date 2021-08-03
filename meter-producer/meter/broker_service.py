from aio_pika import connect_robust, Message

from .utils import get_logger

logger = get_logger(__name__)


class BrokerService:

    def __init__(self, host_url, queue_name):
        self._host_url = host_url
        self._queue_name = queue_name
        self._connection_obj = None
        self._channel = None

    async def connect(self):
        """
        Connect to RabbitMQ broker server
        :return:
        """
        self._connection_obj = await connect_robust(url=self._host_url)
        self._channel = await self._connection_obj.channel()

    async def close(self):
        """
        Close connection with RabbitMQ broker server
        :return:
        """
        await self._connection_obj.close()

    async def send_message(self, data):
        """
        Publish message to Message Queue broker
        :param data:
        """
        logger.info("Published meter value to Message queue")
        await self._channel.default_exchange.publish(
            Message(body=data.encode()),
            routing_key=self._queue_name,
        )
