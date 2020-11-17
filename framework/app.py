from logging import Logger
from typing import Callable, Dict, Tuple, Type, Union


from framework.data.config import Config
from framework.http.request import Request
from framework.http.response import Response, ErrorResponse
from framework.i18n.datetime import DateTime
from framework.i18n.translator import Translator
from framework.lang.annotation import FunctionAnnotation
from framework.lang.di import DI
from framework.lang.dict import Binder
from framework.task.transaction import Transaction


class App:
    __instances: Dict[str, 'App'] = {}

    @classmethod
    def get(cls, name: str) -> 'App':
        return App.__instances[name]

    def __init__(self, name: str, di: DI) -> None:
        self._name = name
        self._di = DI()
        App.__instances[name] = self

    @property
    def config(self) -> dict:
        return self._di.resolve(Config)

    @property
    def logger(self) -> Logger:
        return self._di.resolve(Logger)

    @property
    def request(self) -> Request:
        return self._di.resolve(Request)

    @property
    def trans(self, path: str) -> str:
        translator: Translator = self._di.resolve(Translator)
        return translator.trans(path)

    @property
    def datetime(self) -> DateTime:
        return self._di.resolve(DateTime)

    def error(self, status: int, message: str, errors: Union[Type[Exception], Tuple[Type[Exception], ...]]):
        """
        Usage:
            ```
            @app.error(400, app.trans('http.bad_request'), ValidationError)
            def action(self) -> Response:
                raise ValidationError()

            action()
            > ErrorResponse(status: 400, message: '400 Bad Request', error: ValidationError)
            ```
        """
        def decorator(wrapper_func: Callable[..., Response]):
            def wrapper(*args, **kwargs) -> Response:
                try:
                    return wrapper_func(*args, **kwargs)
                except errors as e:
                    return ErrorResponse(status, message, e)

            return wrapper

        return decorator

    def params(self, wrapper_func: Callable[..., Response]):
        """
        Usage:
            ```
            @app.params
            def action(self, params: Params) -> Response:
                print(f'{params}')
                > {'a': 100, 'b': 'hoge', 'c': None}

            @dataclass
            class Params:
                a: int = 0
                b: str = ''
                c: Optional[int] = None
            ```
        """
        def wrapper(*args, **kwargs) -> Response:
            func_anno = FunctionAnnotation(wrapper_func)
            binded_args = {
                key: Binder(self.request.params).bind(arg_anno.origin)
                for key, arg_anno in func_anno.args.items()
            }
            return wrapper_func(**binded_args)

        return wrapper

    def transaction(self, error_handler: Callable[[Exception, dict], None]):
        """
        Usage:
            def action(self) -> Response:
                with app.transaction(self.rollback):
                    publish_id = Model.create()
                    raise ValueError()

            def rollback(self, error: Exception, context: dict):
                print(error)
                > ValueError

                print(context)
                > {'publish_id': 100}
        """
        return Transaction(error_handler)
