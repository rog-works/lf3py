from types import FunctionType
from typing import Any, Callable, Dict, Type, Union

from framework.lang.annotation import FunctionAnnotation


class DI:
    def __init__(self) -> None:
        self._injectors: Dict[Type, Union[Type, Callable]] = {}
        self._instances: Dict[Type, Any] = {}

    def register(self, symbol: Type, injector: Union[Type, Callable]):
        self._injectors[symbol] = injector

    def resolve(self, symbol: Type) -> Any:
        if symbol not in self._injectors:
            raise ValueError()

        if symbol in self._instances:
            return self._instances[symbol]

        injector = self._injectors[symbol]
        anno = FunctionAnnotation(injector if isinstance(injector, FunctionType) else injector.__init__)
        args = {key: self.resolve(arg_anno.origin) for key, arg_anno in anno.args.items()}
        instance = injector(**args)
        self._instances[symbol] = instance
        return instance
