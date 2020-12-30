from typing import Type, TypeVar

from lf3py.app.provider import locator
from lf3py.aws.types import LambdaEvent
from lf3py.config import ModuleDefinitions
from lf3py.lang.locator import ILocator
from lf3py.middleware.middleware import ErrorMiddleware, Middleware, PerformMiddleware
from lf3py.task.types import RunnerDecorator
from lf3py.session import Session

_T = TypeVar('_T', bound='App')


class App:
    @classmethod
    def module_definitions(cls) -> ModuleDefinitions:
        raise NotImplementedError()

    @classmethod
    def blueprint(cls: Type[_T], name: str) -> _T:
        Session.add_context(name, cls())
        return Session.context(name)

    @classmethod
    def entry(cls: Type[_T], event: dict) -> _T:
        app = cls()
        app._locator.register(LambdaEvent, lambda: event)
        Session.add_context('__root__', app)
        return app

    @classmethod
    def get(cls: Type[_T], name: str = '__root__') -> _T:
        return Session.context(name)

    def __init__(self) -> None:
        self._locator = locator(self.module_definitions())

    @property
    def locator(self) -> ILocator:
        return self._locator

    @property
    def middleware(self) -> Middleware:
        return self._locator.resolve(Middleware)

    def behavior(self, *perform_middlewares: PerformMiddleware) -> RunnerDecorator:
        return self.middleware.attach(*perform_middlewares)

    def on_error(self, *error_handlers: ErrorMiddleware) -> RunnerDecorator:
        return self.middleware.error(*error_handlers)
