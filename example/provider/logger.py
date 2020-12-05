import logging

from framework.data.config import Config
from framework.lang.module import load_module


def make_logger(config: Config) -> logging.Logger:
    log_config = config['logger']

    logger = logging.getLogger(__name__)
    logger.setLevel(log_config['level'])

    func_name = log_config['module']
    func_args = log_config['modules'][func_name]
    base_args = {'level': log_config['level'], 'format': log_config['format']}
    kwargs = {**base_args, **func_args}
    handler: logging.Handler = load_module(__name__, func_name)(**kwargs)
    logger.addHandler(handler)
    return logger


def file_handler(path: str, level: str, format: str) -> logging.Handler:
    handler = logging.FileHandler(path)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(format))
    return handler
