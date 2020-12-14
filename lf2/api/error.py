from typing import Callable, List, Type

from lf2.api.errors import ApiError
from lf2.api.types import ErrorDefinition
from lf2.lang.sequence import first, flatten
from lf2.task.result import Result
from lf2.task.runner import Runner, RunnerDecorator


class ApiErrorHandler:
    def __call__(self, status: int, message: str, *handle_errors: Type[Exception]) -> RunnerDecorator:
        """
        Examples:
            >>> @app.error(400, app.18n.trans('http.400'), ValidationError)
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
                    raise ApiError(message, status) from e

            return wrapper

        return decorator
