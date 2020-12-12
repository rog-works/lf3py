from abc import ABCMeta, abstractmethod
from typing import Any

from lf2.lang.annotation import ClassAnnotation, PropertyAnnotation
from lf2.lang.error import raises
from lf2.serialization.errors import SerializeError


class Serializer(metaclass=ABCMeta):
    @abstractmethod
    def serialize(self, obj: Any) -> Any:
        raise NotImplementedError()


class DictSerializer(Serializer):
    @raises(SerializeError, TypeError)
    def serialize(self, obj: Any) -> dict:
        obj_anno = ClassAnnotation(type(obj))
        return {
            key: self.__serialize_value(prop_anno, getattr(obj, key))
            for key, prop_anno in obj_anno.properties.items()
            if not key.startswith('_')
        }

    def __serialize_value(self, prop_anno: PropertyAnnotation, value: Any) -> Any:
        if prop_anno.is_primitive:
            return value
        elif prop_anno.origin is list:
            return [self.__serialize_value(prop_anno.list_value, in_value) for in_value in value]
        elif prop_anno.origin is dict:
            return {key: self.__serialize_value(prop_anno.dict_value, in_value) for key, in_value in value.items()}
        elif prop_anno.is_union:
            return self.__try_serialize_union_value(prop_anno, value)
        elif prop_anno.is_enum:
            return value.value
        else:
            return self.serialize(value)

    def __try_serialize_union_value(self, prop_anno: PropertyAnnotation, value: Any) -> Any:
        for candidate in prop_anno.union_values:
            if candidate.origin is type(value):
                return self.__serialize_value(candidate, value)

        raise TypeError(f'Unresolved value type. type = {prop_anno.origin}')
