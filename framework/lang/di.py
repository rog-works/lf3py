from typing import Any, Callable, Dict, Type, Union

from framework.lang.annotation import FunctionAnnotation


class DI:
    def __init__(self) -> None:
        self._injectors: Dict[Type, Union[Type, Callable]] = {}
        self._instances: Dict[Type, Any] = {}

    def register(self, from_type: Type, injector: Union[Type, Callable]):
        self._injectors[from_type] = injector

    def resolve(self, from_type: Type) -> Any:
        if from_type not in self._injectors:
            raise ValueError()

        if from_type in self._instances:
            return self._instances[from_type]

        injector = self._injectors[from_type]
        anno = FunctionAnnotation(injector if injector is callable else injector.__init__)
        args = {key: self.resolve(arg_anno.origin) for key, arg_anno in anno.args.items()}
        instance = injector(**args)
        self._instances[from_type] = instance
        return instance
