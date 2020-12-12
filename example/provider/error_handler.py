from framework.api.types import ErrorHandler

from example.api.error_handler import dev_handler, prd_handler


def make_dev_handler() -> ErrorHandler:
    return dev_handler


def make_prd_handler() -> ErrorHandler:
    return prd_handler
