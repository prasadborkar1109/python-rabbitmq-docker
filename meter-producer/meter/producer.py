import time
from random import randrange

from .utils import get_logger

logger = get_logger(__name__)


class MeterProducer:

    def __init__(self, min_value: int, max_value: int, broker, publish_time_interval):
        self._min_value = min_value
        self._max_value = max_value
        self._broker = broker
        self._publish_time_interval = publish_time_interval

    def generate_meter_value(self):
        """
        Generate random value (meter value) between given range in Kilowatt
        :return:
        """
        return randrange(self._min_value, self._max_value)

    async def produce_data(self):
        """
        Publish meter value to Message Queue
        :return:
        """
        while True:
            meter_value = self.generate_meter_value()
            logger.info("Meter produced value in watts: " + str(meter_value))
            await self._broker.send_message(str(meter_value))
            time.sleep(self._publish_time_interval)

    async def connect_to_broker(self):
        """
        Producer connecting to broker server
        """
        await self._broker.connect()

    async def close_broker_connection(self):
        """
        Producer closing broker connection
        """
        await self._broker.close()
