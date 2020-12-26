from typing import Callable

from lf3py.config import ModuleDefinitions
from lf3py.lang.di import DI
from lf3py.middleware import attach
from lf3py.middleware.types import ErrorMiddlewares, Middleware


class App:
    @classmethod
    def module_definitions(cls) -> ModuleDefinitions:
        raise NotImplementedError()

    def __init__(self, di: DI) -> None:
        self._di = di

    def behavior(self, *middlewares: Middleware, error: ErrorMiddlewares = tuple()) -> Callable[[Callable], Callable]:
        return attach(self._di, *middlewares, error=error)
