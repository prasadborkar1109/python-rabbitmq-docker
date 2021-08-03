from aio_pika import connect_robust


class BrokerService:

    def __init__(self, host_url, queue_name):
        self._host_url = host_url
        self._queue_name = queue_name
        self._connection_obj = None
        self._channel = None
        self._queue = None

    async def connect(self):
        """
        Connect to RabbitMQ broker server
        :return:
        """
        self._connection_obj = await connect_robust(url=self._host_url)
        self._channel = await self._connection_obj.channel()
        self._queue = await self._channel.declare_queue(self._queue_name, auto_delete=True)

    async def close(self):
        """
        Close connection with RabbitMQ broker server
        """
        await self._connection_obj.close()

    async def receive_data(self, consumer):
        await self._queue.consume(consumer.data_received)
