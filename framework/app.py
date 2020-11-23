from logging import Logger
from typing import Callable, Dict, Tuple, Type, Union


from framework.data.config import Config
from framework.http.data import Request, Response
from framework.task.result import Result
from framework.i18n.locale import Locale
from framework.lang.annotation import FunctionAnnotation
from framework.lang.di import DI
from framework.lang.error import stacktrace
from framework.lang.object import Assigner
from framework.task.runner import Runner
from framework.task.transaction import Transaction


class App:
    __instances: Dict[str, 'App'] = {}

    @classmethod
    def get(cls, name: str) -> 'App':
        return cls.__instances[name]

    def __init__(self, name: str, di: DI) -> None:
        self._name = name
        self._di = di
        self.__instances[name] = self

    @property
    def config(self) -> dict:
        return self._di.resolve(Config)

    @property
    def locale(self) -> Locale:
        return self._di.resolve(Locale)

    @property
    def logger(self) -> Logger:
        return self._di.resolve(Logger)

    @property
    def request(self) -> Request:
        return self._di.resolve(Request)

    @property
    def response(self) -> Response:
        return self._di.resolve(Response)

    def run(self) -> Result:
        runner: Runner = self._di.resolve(Runner)
        return runner()

    def success(self, body: dict, status: int = 200) -> Response:
        return self.http_result(status, body)

    def http_result(self, status: int, body: dict) -> Response:
        return Response(status=status, headers=self.response.headers, body=body)

    def error_500(self, error: Exception) -> Response:
        return self.error_result(500, self.locale.trans('http.500'), error)

    def error_result(self, status: int, message: str, error: Exception) -> Response:
        body = {'message': message, 'stacktrace': stacktrace(error)}
        return self.http_result(status, body)

    def error(self, status: int, message: str, handle_errors: Union[Type[Exception], Tuple[Type[Exception], ...]]):
        """
        Usage:
            ```
            @app.error(400, app.locale.trans('http.400'), ValidationError)
            def action(self) -> Result:
                raise ValidationError()

            action()
            > Result(status: 400, message: '400 Bad Request', error: ValidationError)
            ```
        """
        def decorator(runner: Callable[..., Result]):
            def wrapper(*args, **kwargs) -> Result:
                try:
                    return runner(*args, **kwargs)
                except handle_errors as e:
                    return self.error_result(status, message, e)

            return wrapper

        return decorator

    def params(self, runner: Callable[..., Result]):
        """
        Usage:
            ```
            @dataclass
            class Params:
                a: int = 0
                b: str = ''
                c: Optional[int] = None

            @app.params
            def action(self, params: Params) -> Result:
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

    def transaction(self, error_handler: Callable[[BaseException, dict], None]):
        """
        Usage:
            def action(self) -> Response:
                with app.transaction(error_handler=self.rollback):
                    publish_id = Model.create()
                    raise ValueError()

            def rollback(self, error: BaseException, context: dict):
                print(error)
                > ValueError

                print(context)
                > {'publish_id': 100}
        """
        return Transaction(error_handler=error_handler)
