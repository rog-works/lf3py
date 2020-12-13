from typing import Callable, List, Type

from lf2.api.data import ErrorBody, Response
from lf2.api.types import ErrorDefinition
from lf2.lang.error import stacktrace
from lf2.lang.sequence import first, flatten
from lf2.task.result import Result
from lf2.task.runner import Runner, RunnerDecorator
from lf2.view.presenter import Presenter


class HTTPPresenter(Presenter):
    def __init__(self, response: Response) -> None:
        self._response = response

    def http_result(self, status: int = 200, body: Result = Result()) -> Response:
        return Response(statusCode=status, headers=self._response.headers, body=body)


class ApiOkPresenter(HTTPPresenter):
    def __call__(self, status: int = 200, body: Result = Result()) -> Response:
        return self.http_result(status, body)


class ApiErrorPresenter(HTTPPresenter):
    def __call__(self, error: Exception) -> Response:
        return self._error_result(500, '500 Internal Server Error', error)

    def _error_result(self, status: int, message: str, error: Exception) -> Response:
        return self.http_result(status, self._build_error_body(status, message, error))

    def _build_error_body(self, status: int, message: str, error: Exception) -> Result:
        return ErrorBody(message=message, stacktrace=stacktrace(error))

    def handle(self, status: int, message: str, *handle_errors: Type[Exception]) -> RunnerDecorator:
        """
        Examples:
            >>> @app.error.handle(400, app.18n.trans('http.400'), ValidationError)
            >>> def action() -> Result:
            >>>     raise ValidationError()

            >>> action().serialize()
            {'status': 400, 'headers': {...}, 'body': {'message': '400 Bad Request', 'stacktrace': [...]}
        """
        return self.handles([(status, message, handle_errors)])

    def define(self, status: int, message: str, *handle_errors: Type[Exception]) -> ErrorDefinition:
        return (status, message, handle_errors)

    def custom(self, wrapper_func: Callable[..., List[ErrorDefinition]]) -> Callable[..., RunnerDecorator]:
        """
        Examples:
            >>> @app.error.custom
            >>> def errors_with(*statuses: int) -> List[ErrorDefinition]:
            >>>     defs = [
            >>>         app.error.define(401, app.i18n.trans('http.401'), UnauthorizedError),
            >>>         app.error.define(503, app.i18n.trans('http.503'), ServiceUnavailableError),
            >>>     ]
            >>>     return [(status, message, errors) for status, message, errors in defs if status in statuses)]

            >>> @errors_with(401, 503)
            >>> def action() -> Response:
            >>>     raise UnauthorizedError()

            >>> action().serialize()
            {'status': 400, 'headers': {...}, 'body': {'message': '401 Unauthorized', 'stacktrace': [...]}
        """
        def wrapper(*args, **kwargs) -> RunnerDecorator:
            return self.handles(wrapper_func(*args, **kwargs))

        return wrapper

    def handles(self, error_defs: List[ErrorDefinition]) -> RunnerDecorator:
        def decorator(runner: Runner) -> Runner:
            def wrapper(*args, **kwargs) -> Result:
                handle_errors = tuple(flatten([errors for _, _, errors in error_defs]))
                try:
                    return runner(*args, **kwargs)
                except handle_errors as e:
                    status, message = first([(status, message) for status, message, errors in error_defs if type(e) in errors])
                    return self._error_result(status, message, e)

            return wrapper

        return decorator
