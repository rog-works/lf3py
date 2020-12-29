from typing import Any, Callable, Dict, Type, TypeVar, Union

from lf3py.di.function import invoke
from lf3py.locator.types import ILocator

_T = TypeVar('_T')


class DI(ILocator):
    def __init__(self) -> None:
        self._injectors: Dict[Type, Union[Type, Callable]] = {}
        self._instances: Dict[Type, Any] = {}

    def can_resolve(self, symbol: Type) -> bool:
        return symbol in self._injectors

    def register(self, symbol: Type, injector: Union[Type, Callable]):
        self._injectors[symbol] = injector

    def resolve(self, symbol: Type[_T]) -> _T:
        if symbol not in self._injectors:
            raise ModuleNotFoundError(f'Unresolved symbol. symbol = {symbol}')

        if symbol in self._instances:
            return self._instances[symbol]

        injector = self._injectors[symbol]
        instance = invoke(self, injector)
        self._instances[symbol] = instance
        return instance
