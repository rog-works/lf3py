from typing import Type, TypeVar
from typing_extensions import Protocol


T_INST = TypeVar('T_INST')


class Locator(Protocol):
    def can_resolve(self, symbol: Type) -> bool:
        raise NotImplementedError()

    def resolve(self, symbol: Type[T_INST]) -> T_INST:
        raise NotImplementedError()
