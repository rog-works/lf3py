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
        found_symbol = self.__resolve_symbol(symbol)
        if found_symbol in self._instances:
            return self._instances[found_symbol]

        injector = self._injectors[found_symbol]
        instance = invoke(self, injector)
        self._instances[symbol] = instance
        return instance

    def __resolve_symbol(self, symbol: Type) -> Type:
        for in_symbol in self._injectors.keys():
            if in_symbol == symbol:
                return in_symbol
            elif hasattr(in_symbol, '__origin__'):
                try:
                    if issubclass(in_symbol.__origin__, symbol):
                        return in_symbol
                except TypeError as e:
                    raise e
            elif issubclass(in_symbol, symbol):
                return in_symbol

        raise ModuleNotFoundError(f'Unresolved symbol. symbol = {symbol}')