import logging

from lf3py.config import Config
from lf3py.i18n.i18n import I18n
from lf3py.logging.formatter import JsonFormatter
from lf3py.logging.cleaner import clear_handler

from example.bpapi.data.context import MyContext


def dev_logger(config: Config, i18n: I18n, context: MyContext) -> logging.LoggerAdapter:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    clear_handler(logger)

    _config = config['logger']['dev_handler']
    handler = logging.FileHandler(_config['path'])
    handler.setLevel(_config['level'])
    handler.setFormatter(JsonFormatter(_config['keys'], tz=i18n.datetime.tz))

    logger.addHandler(handler)
    return logging.LoggerAdapter(logger, {'context': context})
