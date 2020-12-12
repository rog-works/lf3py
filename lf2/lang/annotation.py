from enum import Enum
from typing import Callable, Dict, List, Type, Union


class ValueAnnotation:
    def __init__(self, value_type: Type) -> None:
        self._type = value_type

    @property
    def is_enum(self) -> bool:
        return type(self._type) is type(Enum)

    @property
    def is_union(self) -> bool:
        return getattr(self._type, '__origin__', type(None)) is Union

    @property
    def is_optional(self) -> bool:
        return type(None) in self.types

    @property
    def is_primitive(self) -> bool:
        return self._type in [int, float, bool, str]

    @property
    def list_value(self) -> 'ValueAnnotation':
        return ValueAnnotation(self.types[0])

    @property
    def dict_value(self) -> 'ValueAnnotation':
        return ValueAnnotation(self.types[1])

    @property
    def union_values(self) -> List['ValueAnnotation']:
        return [ValueAnnotation(candidate_type) for candidate_type in self.types]

    @property
    def origin(self) -> Type:
        return getattr(self._type, '__origin__', self._type)

    @property
    def org_type(self) -> Type:
        return self._type

    @property
    def types(self) -> List[Type]:
        return getattr(self._type, '__args__', [self._type])

    @property
    def enum_members(self) -> Dict[str, Enum]:
        return getattr(self.origin, '__members__', {})


PropertyAnnotation = ValueAnnotation
ArgAnnotation = ValueAnnotation


class FunctionAnnotation:
    def __init__(self, func: Callable) -> None:
        self._func = func

    @property
    def is_method(self) -> bool:
        return hasattr(self._func, '__self__')

    @property
    def args(self) -> Dict[str, ArgAnnotation]:
        if not hasattr(self._func, '__annotations__'):
            return {}

        return {key: ArgAnnotation(arg) for key, arg in self._func.__annotations__.items() if key != 'return'}

    @property
    def returns(self) -> ValueAnnotation:
        if not hasattr(self._func, '__annotations__'):
            return ValueAnnotation(type(None))

        return ValueAnnotation(self._func.__annotations__['return'])


class ClassAnnotation:
    def __init__(self, class_type: Type) -> None:
        self._type = class_type

    @property
    def origin(self) -> Type:
        return self._type

    @property
    def constructor(self) -> FunctionAnnotation:
        return FunctionAnnotation(self.origin.__init__)

    @property
    def properties(self) -> Dict[str, PropertyAnnotation]:
        if not hasattr(self._type, '__annotations__'):
            return {}

        return {key: PropertyAnnotation(prop) for key, prop in self._type.__annotations__.items()}
