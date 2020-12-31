from typing import Type, TypeVar

from lf3py.app.provider import di_container
from lf3py.aws.types import LambdaEvent
from lf3py.config import ModuleDefinitions
from lf3py.lang.locator import Locator
from lf3py.middleware.middleware import ErrorMiddleware, Middleware, PerformMiddleware
from lf3py.session.session import Session
from lf3py.task.types import RunnerDecorator

T_APP = TypeVar('T_APP', bound='App')


class App:
    @classmethod
    def entry(cls: Type[T_APP], event: dict) -> T_APP:
        di = di_container(cls.module_definitions())
        di.register(LambdaEvent, lambda: event)
        app = cls(di)
        return app

    @classmethod
    def blueprint(cls: Type[T_APP]) -> T_APP:
        di = di_container(cls.module_definitions())
        return cls(di)

    @classmethod
    def module_definitions(cls) -> ModuleDefinitions:
        raise NotImplementedError()

    def __init__(self, locator: Locator) -> None:
        self._locator = locator

    def start(self) -> Session:
        return Session.start(self._locator)

    @property
    def middleware(self) -> Middleware:
        return self._locator.resolve(Middleware)

    def behavior(self, *perform_middlewares: PerformMiddleware) -> RunnerDecorator:
        return self.middleware.effect(*perform_middlewares)

    def on_error(self, *error_handlers: ErrorMiddleware) -> RunnerDecorator:
        return self.middleware.catch(*error_handlers)
