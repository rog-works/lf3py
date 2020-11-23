from enum import Enum
from typing import Callable, Dict, List, Type, Union


class FunctionAnnotation:
    def __init__(self, func: Callable) -> None:
        self._func = func

    @property
    def is_method(self) -> bool:
        return hasattr(self._func, '__self__')

    @property
    def args(self) -> Dict[str, 'ArgAnnotation']:
        if not hasattr(self._func, '__annotations__'):
            return {}

        return {key: ArgAnnotation(arg) for key, arg in self._func.__annotations__.items() if key != 'return'}

    @property
    def returns(self) -> 'ValueAnnotation':
        if not hasattr(self._func, '__annotations__'):
            return ValueAnnotation(type(None))

        return ValueAnnotation(self._func.__annotations__['return'])


class ClassAnnotation:
    def __init__(self, klass: Type) -> None:
        self._klass = klass

    @property
    def origin(self) -> Type:
        return self._klass

    @property
    def constructor(self) -> FunctionAnnotation:
        return FunctionAnnotation(self.origin.__init__)

    @property
    def properties(self) -> Dict[str, 'PropertyAnnotation']:
        if not hasattr(self._klass, '__annotations__'):
            return {}

        return {key: PropertyAnnotation(prop) for key, prop in self._klass.__annotations__.items()}


class ValueAnnotation:
    def __init__(self, prop: Type) -> None:
        self._prop = prop

    @property
    def is_enum(self) -> bool:
        return type(self._prop) is type(Enum)

    @property
    def is_union(self) -> bool:
        if not hasattr(self._prop, '__origin__'):
            return False

        return self._prop.__origin__ is Union

    @property
    def is_optional(self) -> bool:
        return type(None) in self.types

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
