from typing import Tuple, Type, Union

from framework.http.data import Request, Response
from framework.i18n.locale import Locale
from framework.lang.annotation import FunctionAnnotation
from framework.lang.error import stacktrace
from framework.lang.object import Assigner
from framework.task.result import Result
from framework.task.runner import Runner


class Api:
    def __init__(self, request: Request, response: Response, locale: Locale) -> None:
        self._request = request
        self._response = response
        self._locale = locale

    @property
    def request(self) -> Request:
        return self._request

    @property
    def response(self) -> Response:
        return self._response

    def success(self, body: dict, status: int = 200) -> Response:
        return self.http_result(status, body)

    def http_result(self, status: int, body: dict) -> Response:
        return Response(status=status, headers=self.response.headers, body=body)

    def error_500(self, error: Exception) -> Response:
        return self.error_result(500, self._locale.trans('http.500'), error)

    def error_result(self, status: int, message: str, error: Exception) -> Response:
        body = {'message': message, 'stacktrace': stacktrace(error)}
        return self.http_result(status, body)

    def error(self, status: int, message: str, handle_errors: Union[Type[Exception], Tuple[Type[Exception], ...]]):
        """
        Usage:
            ```
            @app.api.error(400, app.locale.trans('http.400'), ValidationError)
            def action() -> Result:
                raise ValidationError()

            action()
            > Result({'status': 400, 'headers': {...}, 'body': {'message': '400 Bad Request', 'stacktrace': [...]})
            ```
        """
        def decorator(runner: Runner):
            def wrapper(*args, **kwargs) -> Result:
                try:
                    return runner(*args, **kwargs)
                except handle_errors as e:
                    return self.error_result(status, message, e)

            return wrapper

        return decorator

    def params(self, runner: Runner):
        """
        Usage:
            ```
            @dataclass
            class Params:
                a: int = 0
                b: str = ''
                c: Optional[int] = None

            @app.api.params
            def action(params: Params) -> Result:
                print(f'{params.__dict__}')
                > {'a': 100, 'b': 'hoge', 'c': None}
            ```
        """
        def wrapper(*args, **kwargs) -> Result:
            func_anno = FunctionAnnotation(runner)
            assigned_args = {
                key: Assigner.assign(arg_anno.origin, self.request.params)
                for key, arg_anno in func_anno.args.items()
            }
            if func_anno.is_method:
                _args = (args[0])
                return runner(*_args, **assigned_args)
            else:
                return runner(**assigned_args)

        return wrapper
