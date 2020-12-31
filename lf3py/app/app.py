from typing import Any, Type, TypeVar

from lf3py.app.provider import locator
from lf3py.aws.types import LambdaEvent
from lf3py.config import ModuleDefinitions
from lf3py.middleware.middleware import ErrorMiddleware, Middleware, PerformMiddleware
from lf3py.task.types import RunnerDecorator

_T = TypeVar('_T', bound='App')


class App:
    __root: Any

    @classmethod
    def get(cls: Type[_T]) -> _T:
        return cls.__root

    @classmethod
    def entry(cls: Type[_T], event: dict) -> _T:
        cls.__root = cls()
        cls.__root._locator.register(LambdaEvent, lambda: event)
        return cls.__root

    @classmethod
    def blueprint(cls: Type[_T]) -> _T:
        return cls()

    @classmethod
    def module_definitions(cls) -> ModuleDefinitions:
        raise NotImplementedError()

    def __init__(self) -> None:
        self._locator = locator(self.module_definitions())

    @property
    def middleware(self) -> Middleware:
        return self._locator.resolve(Middleware)

    def behavior(self, *perform_middlewares: PerformMiddleware) -> RunnerDecorator:
        return self.middleware.effect(*perform_middlewares)

    def on_error(self, *error_handlers: ErrorMiddleware) -> RunnerDecorator:
        return self.middleware.catch(*error_handlers)
