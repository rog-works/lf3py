import logging

from lf2.data.config import Config


def dev_logger(config: Config) -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    _config = config['logger']['dev_handler']
    handler = logging.FileHandler(_config['path'])
    handler.setLevel(_config['level'])
    handler.setFormatter(logging.Formatter(_config['format']))

    logger.addHandler(handler)
    return logger
