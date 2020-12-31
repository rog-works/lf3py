from typing import Dict, List

from lf3py.api.errors import ApiError, BadRequestError, DataNotFoundError, UnsupportedMediaTypeError
from lf3py.middleware.types import ErrorMiddleware
from lf3py.routing.errors import DispatchError, RouteMismatchError


def route_mismatch(error: Exception, *args):
    if isinstance(error, RouteMismatchError):
        raise DataNotFoundError() from error


def unexpected_dispach(error: Exception, *args):
    if isinstance(error, DispatchError):
        raise BadRequestError() from error


def error_400(error: Exception, *args):
    if isinstance(error, BadRequestError):
        raise ApiError('400 Bad Request', 400) from error


def error_404(error: Exception, *args):
    if isinstance(error, DataNotFoundError):
        raise ApiError('404 Data Not Found', 404) from error


def error_415(error: Exception, *args):
    if isinstance(error, UnsupportedMediaTypeError):
        raise ApiError('415 Unsupported Media Type', 415) from error


def within(*statuses: int) -> List[ErrorMiddleware]:
    handlers: Dict[int, ErrorMiddleware] = {
        400: error_400,
        404: error_404,
        415: error_415,
    }
    return [handler for status, handler in handlers.items() if status in statuses]
