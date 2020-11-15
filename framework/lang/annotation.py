from enum import Enum
from typing import Callable, Dict, List, Type, Union


class FunctionAnnotation:
    def __init__(self, func: Callable) -> None:
        self._func = func

    @property
    def args(self) -> Dict[str, 'ArgAnnotation']:
        return {key: ArgAnnotation(arg) for key, arg in self._func.__annotations__.items()}


class ClassAnnotation:
    def __init__(self, klass: Type) -> None:
        self._klass = klass

    @property
    def origin(self) -> Type:
        return self._klass

    @property
    def properties(self) -> Dict[str, 'PropertyAnnotation']:
        return {key: PropertyAnnotation(prop) for key, prop in self._klass.__annotations__.items()}


class ValueAnnotation:
    def __init__(self, prop: Type) -> None:
        self._prop = prop

    @property
    def is_int(self) -> bool:
        return self.origin is int

    @property
    def is_float(self) -> bool:
        return self.origin is float

    @property
    def is_bool(self) -> bool:
        return self.origin is bool

    @property
    def is_str(self) -> bool:
        return self.origin is str

    @property
    def is_enum(self) -> bool:
        return issubclass(self._prop, Enum)

    @property
    def is_union(self) -> bool:
        return self.origin is Union

    @property
    def is_optional(self) -> bool:
        return self.types in type(None)

    @property
    def origin(self) -> Type:
        return self._prop.__origin__ if self.is_union else self._prop

    @property
    def types(self) -> List[Type]:
        return self._prop.__args__ if self.is_union else [self._prop]

    @property
    def enum_members(self) -> Dict[str, Enum]:
        return self.origin.__members__


class PropertyAnnotation(ValueAnnotation):
    pass


class ArgAnnotation(ValueAnnotation):
    pass
