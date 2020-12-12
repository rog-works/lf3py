from types import FunctionType
from typing import Any, Callable, Dict, Type, TypeVar, Union

from lf2.lang.annotation import FunctionAnnotation

_T = TypeVar('_T')


class DI:
    def __init__(self) -> None:
        self._injectors: Dict[Type, Union[Type, Callable]] = {}
        self._instances: Dict[Type, Any] = {}

    def register(self, symbol: Type, injector: Union[Type, Callable]):
        self._injectors[symbol] = injector

    def resolve(self, symbol: Type[_T]) -> _T:
        if symbol not in self._injectors:
            raise ModuleNotFoundError(f'Unresolved symbol. symbol = {symbol}')

        if symbol in self._instances:
            return self._instances[symbol]

        injector = self._injectors[symbol]
        anno = FunctionAnnotation(injector if isinstance(injector, FunctionType) else injector.__init__)
        kwargs = {key: self.resolve(arg_anno.org_type) for key, arg_anno in anno.args.items()}
        instance = injector(**kwargs)
        self._instances[symbol] = instance
        return instance
