from typing import Dict, List, Optional

from lf3py.api.errors import (
    ApiError,
    BadRequestError,
    DataNotFoundError,
    NotAcceptableError,
    UnsupportedMediaTypeError,
)
from lf3py.i18n import I18n
from lf3py.middleware.types import CatchMiddleware
from lf3py.openapi.schema import embed


@embed.responses(400, {'description': '400 Bad Request'})
def bad_request(error: Exception, i18n: Optional[I18n] = None, *args):
    if isinstance(error, BadRequestError):
        raise ApiError(('400 Bad Request' if not i18n else i18n.trans('http.400')), 400) from error


@embed.responses(404, {'description': '404 Data Not Found'})
def data_not_found(error: Exception, i18n: Optional[I18n] = None, *args):
    if isinstance(error, DataNotFoundError):
        raise ApiError(('404 Data Not Found' if not i18n else i18n.trans('http.404')), 404) from error


@embed.responses(406, {'description': '406 Not Acceptable'})
def not_acceptable(error: Exception, i18n: Optional[I18n] = None, *args):
    if isinstance(error, NotAcceptableError):
        raise ApiError(('406 Not Acceptable' if not i18n else i18n.trans('http.406')), 406) from error


@embed.responses(415, {'description': '415 Unsupported Media Type'})
def unsupported_media_type(error: Exception, i18n: Optional[I18n] = None, *args):
    if isinstance(error, UnsupportedMediaTypeError):
        raise ApiError(('415 Unsupported Media Type' if not i18n else i18n.trans('http.415')), 415) from error


def on(*statuses: int) -> List[CatchMiddleware]:
    handlers: Dict[int, CatchMiddleware] = {
        400: bad_request,
        404: data_not_found,
        406: not_acceptable,
        415: unsupported_media_type,
    }
    return [handler for status, handler in handlers.items() if status in statuses]
