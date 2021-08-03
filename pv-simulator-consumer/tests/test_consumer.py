import unittest
import asyncio

from pv_simulator.consumer import PVSimulator
from tests.helper import construct_class


class TestConsumer(unittest.TestCase):

    def setUp(self) -> None:
        self.broker = construct_class("BrokerService")
        self.writer = construct_class("FileWriter")
        self._min_range = 0
        self._max_range = 9000
        self.simulator = PVSimulator(min_range=self._min_range, max_range=self._max_range, broker=self.broker,
                                     file_writer=self.writer)

    def test_connect_to_broker(self):
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self.simulator.connect_to_broker())
        loop.close()
        self.assertIsNone(result)

    def test_generate_pv_value(self):
        result = self.simulator.generate_pv_value()
        self.assertIsNotNone(result)
        self.assertGreaterEqual(result, self._min_range)
        self.assertLessEqual(result, self._max_range)
