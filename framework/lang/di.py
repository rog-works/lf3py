from typing import Any, Dict, Type

from framework.lang.annotation import ClassAnnotation


class DI:
    def __init__(self) -> None:
        self._types: Dict[Type, Type] = {}
        self._instances: Dict[Type, Any] = {}

    def register(self, from_type: Type, inject_type: Type):
        self._types[from_type] = inject_type

    def resolve(self, from_type: Type) -> Any:
        if from_type not in self._types:
            raise ValueError()

        if from_type in self._instances:
            return self._instances[from_type]

        ctor = self._types[from_type]
        anno = ClassAnnotation(ctor)
        args = {key: self.resolve(arg_anno.origin) for key, arg_anno in anno.constructor.args.items()}
        instance = ctor(**args)
        self._instances[from_type] = instance
        return instance
