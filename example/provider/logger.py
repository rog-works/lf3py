import logging

from framework.data.config import Config
from framework.lang.module import load_module


def make_logger(config: Config) -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    func_name = config['logger']['module']
    func_args = config['logger']['modules'][func_name]
    logger.addHandler(load_module(__name__, func_name)(**func_args))
    return logger


def file_handler(path: str, level: str, format: str) -> logging.Handler:
    handler = logging.FileHandler(path)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(format))
    return handler
