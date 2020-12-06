from typing import Callable, Type, TypeVar

from framework.lang.di import DI

_T = TypeVar('_T')


class App:
    def __init__(self, di: DI) -> None:
        self._di = di

    def perform(self, runner: Type[Callable[..., _T]], *args, **kwargs) -> _T:
        return (self._di.resolve(runner))(*args, **kwargs)
