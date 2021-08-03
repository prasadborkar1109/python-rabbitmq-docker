import os
import asyncio

from dotenv import load_dotenv

from .consumer import PVSimulator
from .broker_service import BrokerService
from .file_writer import FileWriter
from .utils import get_logger

logger = get_logger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=ENV_FILE_PATH)


async def pv_simulator(loop):
    """
    Function to generate PV value and consume meter value from RabbitMQ message queue
    """
    logger.info('pv simulator started...')
    try:
        broker = BrokerService(host_url=os.getenv("RABBITMQ_DEFAULT_HOST"),
                               queue_name=os.getenv("RABBITMQ_QUEUE_NAME"))

        writer = FileWriter(file_path=os.getenv("OUTPUT_FILE_PATH"))
        consumer = PVSimulator(min_range=int(os.getenv("MIN_VALUE_RANGE")),
                               max_range=int(os.getenv("MAX_VALUE_RANGE")),
                               broker=broker, file_writer=writer)

        # connect to broker server to consume data
        try:
            await consumer.connect_to_broker()
        except OSError as exc:
            logger.error(f"Connection to Broker failed {exc}")
            loop.call_soon_threadsafe(loop.stop)

        await consumer.consume_data()

    except Exception as ex:
        logger.error(f"Error consuming data: {ex}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(pv_simulator(loop))
    loop.run_forever()
