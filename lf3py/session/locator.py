from abc import ABCMeta
from typing import Any, Callable, Type, TypeVar

_T = TypeVar('_T')


class ILocator(metaclass=ABCMeta):
    def resolve(self, symbol: Type[_T]) -> _T:
        raise NotImplementedError()


class Locatorify(ILocator):
    def __init__(self, resolver: Callable[[Type], Any]) -> None:
        self._resolver = resolver

    def resolve(self, symbol: Type[_T]) -> _T:
        return self._resolver(symbol)
