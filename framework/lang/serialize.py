from abc import ABCMeta, abstractmethod
from typing import Any, Type

from framework.lang.annotation import ClassAnnotation, PropertyAnnotation


class Serializer(metaclass=ABCMeta):
    @abstractmethod
    def serialize(self, obj: Type) -> Any:
        raise NotImplementedError()


class DictSerializer(Serializer):
    def serialize(self, obj: Type) -> dict:
        return {key: value for key, value in obj.__dict__.items() if not key.startswith('_')}


class Deserializer(metaclass=ABCMeta):
    @abstractmethod
    def deserialize(self, obj_type: Type, data: Any) -> Any:
        raise NotImplementedError()


class DictDeserializer(Deserializer):
    def deserialize(self, obj_type: Type, data: dict) -> dict:
        obj_anno = ClassAnnotation(obj_type)
        deserialized = (obj_anno.origin)()
        for key, prop_anno in obj_anno.properties.items():
            if not prop_anno.is_optional and key not in data:
                raise ValueError(f'"{key}" is required key. from {obj_type}')

            setattr(deserialized, key, self.__cast_value(prop_anno, data[key]) if key in data else None)

        return deserialized

    def __cast_value(self, prop_anno: PropertyAnnotation, value: Any) -> Any:
        if prop_anno.is_primitive:
            if prop_anno.origin is int:
                return int(value)
            elif prop_anno.origin is float:
                return float(value)
            elif prop_anno.origin is bool:
                return value == 'true' if value in ['true', 'false'] else bool(value)
            else:
                return value
        elif prop_anno.origin is list:
            return [self.__cast_value(prop_anno.iter_value, in_value) for in_value in value]
        elif prop_anno.origin is dict:
            return {key: self.__cast_value(prop_anno.iter_value, in_value) for key, in_value in value.items()}
        elif prop_anno.is_union:
            return self.__cast_value(prop_anno.primary_value, value)
        elif prop_anno.is_enum:
            return (prop_anno.origin)(value)
        else:
            return self.deserialize(prop_anno.origin, value)
