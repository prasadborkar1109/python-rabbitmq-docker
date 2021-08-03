import logging


def get_logger(name: str, log_level: int = 20, log_format: str = None):
    format = log_format or '%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s'
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(log_level)
    return logger
