from typing import NoReturn, Tuple

from lf3py.api.errors import ApiError, BadRequestError, UnsupportedMediaTypeError
from lf3py.i18n import I18n
from lf3py.middleware.types import ErrorMiddleware


def within(*statuses: int) -> Tuple[ErrorMiddleware, ...]:
    def error_400(error: BadRequestError, i18n: I18n) -> NoReturn:
        raise ApiError(i18n.trans('http.400'), 400) from error

    def error_415(error: UnsupportedMediaTypeError, i18n: I18n) -> NoReturn:
        raise ApiError(i18n.trans('http.415'), 415) from error

    handlers = {
        400: error_400,
        415: error_415,
    }
    return tuple([handler for status, handler in handlers.items() if status in statuses])
