from typing import Any, Callable, Dict, Type, TypeVar, Union

from lf3py.lang.annotation import FunctionAnnotation
from lf3py.lang.inspect import default_args

_T = TypeVar('_T')


class DI:
    def __init__(self) -> None:
        self._injectors: Dict[Type, Union[Type, Callable]] = {}
        self._instances: Dict[Type, Any] = {}

    def has(self, symbol: Type) -> bool:
        return symbol in self._injectors

    def register(self, symbol: Type, injector: Union[Type, Callable]):
        self._injectors[symbol] = injector

    def resolve(self, symbol: Type[_T]) -> _T:
        if symbol not in self._injectors:
            raise ModuleNotFoundError(f'Unresolved symbol. symbol = {symbol}')

        if symbol in self._instances:
            return self._instances[symbol]

        injector = self._injectors[symbol]
        instance = self.invoke(injector)
        self._instances[symbol] = instance
        return instance

    def invoke(self, func: Callable[..., _T]) -> _T:
        func_anno, defaults = FunctionAnnotation(func), default_args(func)
        inject_kwargs = {
            key: self.__resolve_arg(key, arg_anno.org_type, defaults)
            for key, arg_anno in func_anno.args.items()
        }
        return func(**inject_kwargs)

    def carrying(self, func: Callable[..., _T]) -> Callable[..., _T]:
        func_anno, defaults = FunctionAnnotation(func), default_args(func)
        inject_kwargs = {
            key: self.__resolve_arg(key, arg_anno.org_type, defaults)
            for key, arg_anno in func_anno.args.items()
            if self.has(arg_anno.org_type) or key in defaults
        }

        def curried_func(*args, **kwargs) -> _T:
            return func(*args, **{**inject_kwargs, **kwargs})

        return curried_func

    def __resolve_arg(self, key: str, symbol: Type, defaults: Dict[str, Any]) -> bool:
        if self.__allow_default(key, symbol, defaults):
            return defaults[key]
        else:
            return self.resolve(symbol)

    def __allow_default(self, key: str, symbol: Type, defaults: Dict[str, Any]) -> bool:
        return not self.has(symbol) and key in defaults
