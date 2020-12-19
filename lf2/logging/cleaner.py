import logging


def clear_handler(logger: logging.Logger):
    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)
