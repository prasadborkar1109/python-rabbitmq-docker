from random import randrange
from datetime import datetime

from .utils import get_logger

logger = get_logger(__name__)


class PVSimulator:

    def __init__(self, min_range: int, max_range: int, broker, file_writer):
        self._min_range = min_range
        self._max_range = max_range
        self._broker = broker
        self._file_writer = file_writer

    def generate_pv_value(self):
        """
        Generate simulated PV value based on min and max range
        """
        return randrange(self._min_range, self._max_range)

    async def consume_data(self):
        """
        Consume data from broker
        """
        await self._broker.receive_data(self)

    async def data_received(self, data):
        meter_value = data.body.decode()
        logger.info(f"PV Simulator consume meter value: {meter_value}")
        pv_value = self.generate_pv_value()

        meter_value_kwatt = int(meter_value) / 1000
        pv_value_kwatt = pv_value / 1000
        combined_value = str(round(meter_value_kwatt + pv_value_kwatt, 3))
        await self._file_writer.write_data([str(datetime.now()), str(meter_value_kwatt), str(pv_value_kwatt),
                                            combined_value])

    async def connect_to_broker(self):
        """
        Producer connecting to broker server
        """
        logger.info("PV Simulator connecting to Message queue")
        await self._broker.connect()

    async def close_broker_connection(self):
        """
        Producer closing broker connection
        """
        logger.info("PV Simulator closing broker connection")
        await self._broker.close()


