from abc import ABCMeta
from typing import Callable, Type, TypeVar, Union

_T = TypeVar('_T')


class ILocator(metaclass=ABCMeta):
    def can_resolve(self, symbol: Type) -> bool:
        raise NotImplementedError()

    def register(self, symbol: Type, resolver: Union[Type, Callable]):
        raise NotImplementedError()

    def resolve(self, symbol: Type[_T]) -> _T:
        raise NotImplementedError()
