import logging

from lf2.data.config import Config
from lf2.i18n.i18n import I18n
from lf2.logging.formatter import JsonFormatter


def dev_logger(config: Config, i18n: I18n) -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    _config = config['logger']['dev_handler']
    handler = logging.FileHandler(_config['path'])
    handler.setLevel(_config['level'])
    handler.setFormatter(JsonFormatter(_config['keys'], tz=i18n.datetime.tz))

    logger.addHandler(handler)
    return logger
