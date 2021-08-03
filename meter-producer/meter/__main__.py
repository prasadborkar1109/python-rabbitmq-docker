import os
import asyncio

from dotenv import load_dotenv

from .producer import MeterProducer
from .broker_service import BrokerService
from .utils import get_logger


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path=ENV_FILE_PATH)

logger = get_logger(__name__)


async def start_meter():
    """
    Function to generate mock home power generation (meter value) and publish to RabbitMQ broker
    """
    logger.info('meter started...')
    try:
        broker = BrokerService(host_url=os.getenv("RABBITMQ_DEFAULT_HOST"),
                               queue_name=os.getenv("RABBITMQ_QUEUE_NAME"))

        producer = MeterProducer(min_value=int(os.getenv("MIN_VALUE_RANGE")),
                                 max_value=int(os.getenv("MAX_VALUE_RANGE")),
                                 broker=broker,
                                 publish_time_interval=2)

        await producer.connect_to_broker()
        await producer.produce_data()

    except KeyboardInterrupt:
        logger.error("User interrupted on going process, stopping meter process")
    except Exception as ex:
        logger.error(f"Error publishing meter value: {ex}")
    finally:
        if producer:
            try:
                await producer.close_broker_connection()
            except Exception as e:
                logger.error(f"Some error is closing broker connection: {e}")


if __name__ == "__main__":
    asyncio.run(start_meter())
