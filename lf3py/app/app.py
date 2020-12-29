from typing import Callable, Type, TypeVar

from lf3py.config import ModuleDefinitions
from lf3py.locator.types import ILocator
from lf3py.middleware import attach
from lf3py.middleware.types import ErrorMiddlewares, Middleware
from lf3py.session import Session


class App:
    @classmethod
    def module_definitions(cls) -> ModuleDefinitions:
        raise NotImplementedError()

    @property
    def _locator(self) -> ILocator:
        return Session.current().locator

    def start(self) -> Session:
        return self._locator.resolve(Session)

    def behavior(self, *middlewares: Middleware, error: ErrorMiddlewares = tuple()) -> Callable[[Callable], Callable]:
        return attach(self._locator, *middlewares, error=error)
