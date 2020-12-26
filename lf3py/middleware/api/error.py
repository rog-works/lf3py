from typing import NoReturn

from lf3py.api.errors import ApiError, BadRequestError, DataNotFoundError, UnsupportedMediaTypeError
from lf3py.middleware.types import ErrorMiddlewares
from lf3py.routing.errors import DispatchError, RouteMismatchError


def route_mismatch(error: RouteMismatchError) -> NoReturn:
    raise DataNotFoundError() from error


def unexpected_dispach(error: DispatchError) -> NoReturn:
    raise BadRequestError() from error


def error_400(error: BadRequestError) -> NoReturn:
    raise ApiError('400 Bad Request', 400) from error


def error_404(error: DataNotFoundError) -> NoReturn:
    raise ApiError('404 Data Not Found', 404) from error


def error_415(error: UnsupportedMediaTypeError) -> NoReturn:
    raise ApiError('415 Unsupported Media Type', 415) from error


def within(*statuses: int) -> ErrorMiddlewares:
    handlers = {
        400: error_400,
        404: error_404,
        415: error_415,
    }
    return tuple([handler for status, handler in handlers.items() if status in statuses])
