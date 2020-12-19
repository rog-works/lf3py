from types import FunctionType
from typing import Any, Callable, Dict, Type, TypeVar, Union

from lf3py.lang.annotation import FunctionAnnotation
from lf3py.lang.inspect import default_args

_T = TypeVar('_T')


class DI:
    def __init__(self) -> None:
        self._injectors: Dict[Type, Union[Type, Callable]] = {}
        self._instances: Dict[Type, Any] = {}

    def register(self, symbol: Type, injector: Union[Type, Callable]):
        self._injectors[symbol] = injector

    def has(self, symbol: Type) -> bool:
        return symbol in self._injectors

    def resolve(self, symbol: Type[_T]) -> _T:
        if symbol not in self._injectors:
            raise ModuleNotFoundError(f'Unresolved symbol. symbol = {symbol}')

        if symbol in self._instances:
            return self._instances[symbol]

        injector = self._injectors[symbol]
        instance = injector(**self._inject_kwargs(injector))
        self._instances[symbol] = instance
        return instance

    def _inject_kwargs(self, injector: Callable) -> dict:
        func_anno = FunctionAnnotation(injector if isinstance(injector, FunctionType) else injector.__init__)
        defaults = default_args(injector)
        kwargs = {}
        for key, arg_anno in func_anno.args.items():
            if not self.has(arg_anno.org_type) and key in defaults:
                kwargs[key] = defaults[key]
            else:
                kwargs[key] = self.resolve(arg_anno.org_type)

        return kwargs
