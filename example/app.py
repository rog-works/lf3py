from logging import Logger
from typing import Callable, Optional

from lf2.api.api import Api
from lf2.api.data import Request
from lf2.app import App as BaseApp
from lf2.aws.aws_lambda.decode import decode_request
from lf2.i18n.i18n import I18n
from lf2.lang.cache import Cache
from lf2.lang.di import DI
from lf2.task.result import Result
from lf2.task.runner import Runner

LambdaHandler = Callable[[dict, object], dict]


class App(BaseApp):
    __instance: Optional['App'] = None

    @classmethod
    def get(cls) -> 'App':
        if cls.__instance is None:
            raise AssertionError()

        return cls.__instance

    def __init__(self, di: DI) -> None:
        super(App, self).__init__(di)
        App.__instance = self

    @property
    def i18n(self) -> I18n:
        return self._di.resolve(I18n)

    @property
    def logger(self) -> Logger:
        return self._di.resolve(Logger)

    @property
    def cache(self) -> Cache:
        return self._di.resolve(Cache)

    @property
    def api(self) -> Api:
        return self._di.resolve(Api)

    def run(self) -> Result:
        return self.perform(Runner)

    def webapi(self, handler: LambdaHandler) -> LambdaHandler:
        def wrapper(event: dict, context: object) -> dict:
            self._di.register(Request, lambda: decode_request(event))
            return handler(event, context)

        return wrapper
