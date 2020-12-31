from typing import Type, TypeVar
from typing_extensions import Protocol


_T = TypeVar('_T')


class Locator(Protocol):
    def can_resolve(self, symbol: Type) -> bool:
        raise NotImplementedError()

    def resolve(self, symbol: Type[_T]) -> _T:
        raise NotImplementedError()
