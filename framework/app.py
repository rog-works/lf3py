from logging import Logger
from typing import Callable, Dict, Tuple, Type, Union


from framework.data.config import Config
from framework.data.http import Request, Response, ErrorResponse
from framework.i18n.locale import Locale
from framework.lang.annotation import FunctionAnnotation
from framework.lang.di import DI
from framework.lang.object import Assigner
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

    def error(self, status: int, message: str, handle_errors: Union[Type[Exception], Tuple[Type[Exception], ...]]):
        """
        Usage:
            ```
            @app.error(400, app.locale.trans('http.400'), ValidationError)
            def action(self) -> Response:
                raise ValidationError()

            action()
            > ErrorResponse(status: 400, message: '400 Bad Request', error: ValidationError)
            ```
        """
        def decorator(action_func: Callable[..., Response]):
            def wrapper(*args, **kwargs) -> Response:
                try:
                    return action_func(*args, **kwargs)
                except handle_errors as e:
                    return ErrorResponse(status, message, e)

            return wrapper

        return decorator

    def params(self, action_func: Callable[..., Response]):
        """
        Usage:
            ```
            @dataclass
            class Params:
                a: int = 0
                b: str = ''
                c: Optional[int] = None

            @app.params
            def action(self, params: Params) -> Response:
                print(f'{params.__dict__}')
                > {'a': 100, 'b': 'hoge', 'c': None}
            ```
        """
        def wrapper(*args, **kwargs) -> Response:
            func_anno = FunctionAnnotation(action_func)
            assigned_args = {
                key: Assigner.assign(arg_anno.origin, self.request.params)
                for key, arg_anno in func_anno.args.items()
            }
            return action_func(args[0], **assigned_args) if func_anno.is_method else action_func(**assigned_args)

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
