from typing import Callable, List, Type

from lf2.api.data import Request, Response
from lf2.api.errors import BadRequestError
from lf2.api.types import ErrorHandler, ErrorDefinition
from lf2.lang.annotation import FunctionAnnotation
from lf2.lang.error import raises
from lf2.lang.sequence import first, flatten
from lf2.serialization.deserializer import DictDeserializer
from lf2.serialization.errors import DeserializeError
from lf2.task.result import Result
from lf2.task.router import Router
from lf2.task.runner import Runner, RunnerDecorator


class Api:
    def __init__(self, request: Request, response: Response, router: Router, error_handler: ErrorHandler) -> None:
        self._request = request
        self._response = response
        self._router = router
        self._error_handler = error_handler

    @property
    def request(self) -> Request:
        return self._request

    @property
    def response(self) -> Response:
        return self._response

    def success(self, status: int = 200, body: Result = Result()) -> Response:
        return self.http_result(status, body)

    def http_result(self, status: int, body: Result) -> Response:
        return Response(statusCode=status, headers=self.response.headers, body=body)

    def error_500(self, error: Exception) -> Response:
        return self.error_result(500, '500 Internal Server Error', error)

    def error_result(self, status: int, message: str, error: Exception) -> Response:
        body = self._error_handler(status, message, error)
        return self.http_result(status, body)

    def error(self, status: int, message: str, *handle_errors: Type[Exception]) -> RunnerDecorator:
        """
        Examples:
            >>> @app.api.error(400, app.18n.trans('http.400'), ValidationError)
            >>> def action() -> Result:
            >>>     raise ValidationError()

            >>> action().serialize()
            {'status': 400, 'headers': {...}, 'body': {'message': '400 Bad Request', 'stacktrace': [...]}
        """
        return self.errors([(status, message, handle_errors)])

    def custom_error(self, wrapper_func: Callable[..., List[ErrorDefinition]]) -> Callable[..., RunnerDecorator]:
        """
        Examples:
            >>> @app.api.custom_error
            >>> def errors_with(*statuses: int) -> List[ErrorDefinition]:
            >>>     defs = [
            >>>         (401, app.i18n.trans('http.401'), (UnauthorizeError,)),
            >>>         (503, app.i18n.trans('http.503'), (ServiceUnavailableError,)),
            >>>     ]
            >>>     return [(status, message, errors) for status, message, errors in defs if status in statuses)]

            >>> @errors_with(401, 503)
            >>> def action() -> Response:
            >>>     raise UnauthorizeError()

            >>> action().serialize()
            {'status': 400, 'headers': {...}, 'body': {'message': '401 Unauthorized', 'stacktrace': [...]}
        """
        def wrapper(*args, **kwargs) -> RunnerDecorator:
            return self.errors(wrapper_func(*args, **kwargs))

        return wrapper

    def errors(self, error_defs: List[ErrorDefinition]) -> RunnerDecorator:
        def decorator(runner: Runner) -> Runner:
            def wrapper(*args, **kwargs) -> Result:
                handle_errors = tuple(flatten([errors for _, _, errors in error_defs]))
                try:
                    return runner(*args, **kwargs)
                except handle_errors as e:
                    status, message = first([(status, message) for status, message, errors in error_defs if type(e) in errors])
                    return self.error_result(status, message, e)

            return wrapper

        return decorator

    def route(self, method: str, path_spec: str) -> RunnerDecorator:
        """
        Examples:
            >>> @app.api.route('GET', '/models')
            >>> def index() -> Response:
            >>>     return app.api.success(body=IndexBody(Model.find_all()))

            >>> @app.api.route('GET', '/models/{id}')
            >>> def show(id: int) -> Response:
            >>>     return app.api.success(body=ShowBody(Model.find(id)))

            >>> @app.api.route('POST', '/models')
            >>> def create(params: CreateParams) -> Response:
            >>>     return app.api.success(body=ShowBody(Model.create(params)))

            >>> @app.api.route('DELETE', '/models/{id}')
            >>> def delete(id: int) -> Response:
            >>>     Models.find(id).delete()
            >>>     return app.api.success()
        """
        def decorator(runner: Runner) -> Runner:
            self._router.register(runner, method, path_spec)

            @raises(BadRequestError, DeserializeError, KeyError, ValueError)
            def wrapper(*args, **kwargs) -> Result:
                dsn = self._router.dsnize(self.request.method, self.request.path)
                func_anno = FunctionAnnotation(runner)

                path_args = dsn.capture(dsn.format(method, path_spec))
                path_args = {
                    key: int(path_args[key]) if arg_anno.origin is int else path_args[key]
                    for key, arg_anno in func_anno.args.items()
                    if key in path_args
                }

                deserializer = DictDeserializer()
                body_args = {
                    key: deserializer.deserialize(arg_anno.origin, self.request.params)
                    for key, arg_anno in func_anno.args.items()
                    if key not in path_args
                }

                inject_kwargs = {**path_args, **body_args}
                if func_anno.is_method:
                    return runner(*(args[0]), **inject_kwargs)
                else:
                    return runner(**inject_kwargs)

            return wrapper

        return decorator
