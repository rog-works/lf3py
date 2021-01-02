from typing import Callable
from typing_extensions import Protocol

AttachMiddleware = Callable[..., None]
"""
Examples:
    >>> # Declaration
    >>> def accept_json(response: Response):
    >>>     if response.headers.get('Accept') != 'application/json':
    >>>         raise UnsupportedMediaTypeError()

    >>> # Usage
    >>> @app.behaivior(accept_json)
    >>> def index() -> Response:
    >>>     ... something ...
"""


class CatchMiddleware(Protocol):
    """
    Examples:
        >>> # Declaration
        >>> def error_400(error: Exception, *args):
        >>>     if isinstance(error, BadRequestError):
        >>>         raise ApiError('400 Bad Request', 400) from error

        >>> def error_415(error: Exception, i18n: I18n, *args):
        >>>     if isinstance(error, UnsupportedMediaTypeError):
        >>>         raise ApiError(i18n.trans('http.415'), 415) from error

        >>> # Usage
        >>> @app.on_error(error_400, error_415)
        >>> def index() -> Response:
        >>>     ... something ...
    """
    def __call__(self, e: Exception, *services):
        raise NotImplementedError()
