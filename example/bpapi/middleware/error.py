from typing import Dict, List

from lf3py.api.errors import ApiError, BadRequestError, UnsupportedMediaTypeError
from lf3py.i18n import I18n
from lf3py.middleware.types import CatchMiddleware


def within(*statuses: int) -> List[CatchMiddleware]:
    def error_400(error: Exception, i18n: I18n, *args):
        if isinstance(error, BadRequestError):
            raise ApiError(i18n.trans('http.400'), 400) from error

    def error_415(error: Exception, i18n: I18n, *args):
        if isinstance(error, UnsupportedMediaTypeError):
            raise ApiError(i18n.trans('http.415'), 415) from error

    handlers: Dict[int, CatchMiddleware] = {
        400: error_400,
        415: error_415,
    }
    return [handler for status, handler in handlers.items() if status in statuses]
