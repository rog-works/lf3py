from abc import ABCMeta, abstractmethod
from typing import Any, Type, TypeVar

from lf3py.lang.annotation import ClassAnnotation, PropertyAnnotation
from lf3py.serialization.errors import DeserializeError

_T = TypeVar('_T')


class Deserializer(metaclass=ABCMeta):
    @abstractmethod
    def deserialize(self, obj_type: Type, data: Any) -> Any:
        raise NotImplementedError()


class DictDeserializer(Deserializer):
    def deserialize(self, obj_type: Type[_T], data: dict) -> _T:
        try:
            obj_anno = ClassAnnotation(obj_type)
            deserialized = (obj_anno.origin)()
            for key, prop_anno in obj_anno.properties.items():
                if not prop_anno.is_optional and key not in data:
                    raise TypeError(f'"{key}" is required key. from {obj_type}')

                setattr(deserialized, key, self.__deserialize_value(prop_anno, data[key]) if key in data else None)

            return deserialized
        except (TypeError, ValueError) as e:
            raise DeserializeError() from e

    def __deserialize_value(self, prop_anno: PropertyAnnotation, value: Any) -> Any:
        if prop_anno.is_primitive:
            if prop_anno.origin is int:
                return int(value)
            elif prop_anno.origin is float:
                return float(value)
            elif prop_anno.origin is bool:
                return value == 'true' if value in ['true', 'false'] else bool(value)
            else:
                return self.__try_deserialize_str_value(value)
        elif prop_anno.origin is list:
            return [self.__deserialize_value(prop_anno.list_value, in_value) for in_value in value]
        elif prop_anno.origin is dict:
            return {key: self.__deserialize_value(prop_anno.dict_value, in_value) for key, in_value in value.items()}
        elif prop_anno.is_union:
            return self.__try_deserialize_union_value(prop_anno, value)
        elif prop_anno.is_enum:
            return (prop_anno.origin)(value)
        else:
            return self.deserialize(prop_anno.origin, value)

    def __try_deserialize_str_value(self, value: Any) -> str:
        if type(value) is str:
            return str(value)

        raise TypeError(f'Unexpected string value. value = {value}')

    def __try_deserialize_union_value(self, prop_anno: PropertyAnnotation, value: Any) -> Any:
        for candidate in prop_anno.union_values:
            try:
                return self.__deserialize_value(candidate, value)
            except (TypeError, ValueError):
                pass

        raise TypeError(f'Unresolved union value type. candidates = {prop_anno.types}')
