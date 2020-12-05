import logging

from framework.data.config import Config


def make_logger(config: Config) -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(str_to_level(config['log_level']))
    return logger


def str_to_level(level: str) -> int:
    mapping = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
    }
    return mapping[level]
