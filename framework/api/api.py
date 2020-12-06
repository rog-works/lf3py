from typing import Callable, List, Type, Tuple

from framework.api.data import ErrorBody, Request, Response
from framework.api.errors import BadRequestError
from framework.api.path import capture_params
from framework.i18n.i18n import I18n
from framework.lang.annotation import FunctionAnnotation
from framework.lang.error import raises, stacktrace
from framework.lang.sequence import first, flatten
from framework.serialization.deserializer import DictDeserializer
from framework.serialization.errors import DeserializeError
from framework.task.result import Result
from framework.task.runner import Runner

ErrorDefinition = Tuple[int, str, Tuple[Type[Exception], ...]]


class Api:
    def __init__(self, request: Request, response: Response, i18n: I18n) -> None:
        self._request = request
        self._response = response
        self._i18n = i18n

    @property
    def request(self) -> Request:
        return self._request

    @property
    def response(self) -> Response:
        return self._response

    def success(self, status: int = 200, body: Result = Result()) -> Response:
        return self.http_result(status, body)

    def http_result(self, status: int, body: Result) -> Response:
        return Response(status=status, headers=self.response.headers, body=body, _serializer=self.response._serializer)

    def error_500(self, error: Exception) -> Response:
        return self.error_result(500, self._i18n.trans('http.500'), error)

    def error_result(self, status: int, message: str, error: Exception) -> Response:
        body = ErrorBody(message=message, stacktrace=stacktrace(error))
        return self.http_result(status, body)

    def error(self, status: int, message: str, *handle_errors: Type[Exception]) -> Callable[[Runner], Runner]:
        """
        Examples:
            >>> @app.api.error(400, app.18n.trans('http.400'), ValidationError)
            >>> def action() -> Result:
            >>>     raise ValidationError()

            >>> action().serialize()
            {'status': 400, 'headers': {...}, 'body': {'message': '400 Bad Request', 'stacktrace': [...]}
        """
        return self.errors([(status, message, handle_errors)])

    def custom_error(self, wrapper_func: Callable[..., List[ErrorDefinition]]) -> Callable[..., Callable[[Runner], Runner]]:
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
        def wrapper(*args, **kwargs) -> Callable[[Runner], Runner]:
            return self.errors(wrapper_func(*args, **kwargs))

        return wrapper

    def errors(self, error_defs: List[ErrorDefinition]) -> Callable[[Runner], Runner]:
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

    def params(self, runner: Runner) -> Runner:
        """
        Examples:
            >>> @dataclass
            >>> class Params:
            >>>     a: int = 0
            >>>     b: str = ''
            >>>     c: Optional[int] = None

            >>> @app.api.params
            >>> def action(params: Params) -> Result:
            >>>     print(f'{params.__dict__}')
            {'a': 100, 'b': 'hoge', 'c': None}
        """
        @raises(BadRequestError, DeserializeError)
        def wrapper(*args, **kwargs) -> Result:
            func_anno = FunctionAnnotation(runner)
            deserializer = DictDeserializer()
            assigned_kwargs = {
                key: deserializer.deserialize(arg_anno.origin, self.request.params)
                for key, arg_anno in func_anno.args.items()
            }
            if func_anno.is_method:
                return runner(*(args[0]), **assigned_kwargs)
            else:
                return runner(**assigned_kwargs)

        return wrapper

    def path_params(self, path_spec: str):
        """
        Examples:
            >>> @app.api.path_params('/models/{id}')
            >>> def action(id: int) -> Result:
            >>>     print(f'id: {id}, type: {type(id)}')
            id: 1234, type: <class 'int'>
        """
        def decorator(runner: Runner) -> Runner:
            @raises(BadRequestError, KeyError)
            def wrapper(*args, **kwargs) -> Result:
                func_anno = FunctionAnnotation(runner)
                params = capture_params(self.request.path, path_spec)
                assigned_kwargs = {
                    key: int(params[key]) if arg_anno.origin is int else params[key]
                    for key, arg_anno in func_anno.args.items()
                }
                if func_anno.is_method:
                    return runner(*(args[0]), **assigned_kwargs)
                else:
                    return runner(**assigned_kwargs)

            return wrapper

        return decorator
