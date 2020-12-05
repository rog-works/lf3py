import logging

from framework.data.config import Config
from framework.lang.module import load_module
from framework.logging.level import str_to_level


def make_logger(config: Config) -> logging.Logger:
    level = str_to_level(config['logger']['level'])
    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    func_name = config['logger']['module']
    func_args = config['logger']['modules'][func_name]
    handler: logging.Handler = load_module(__name__, func_name)(**func_args)
    handler.setLevel(level)
    logger.addHandler(handler)
    return logger


def file_handler(path: str) -> logging.Handler:
    handler = logging.FileHandler(path)
    return handler
