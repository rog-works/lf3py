from typing import Any, List, Type, TypeVar
import re

from framework.lang.annotation import ClassAnnotation, PropertyAnnotation


Node = TypeVar('Node', int, float, str, dict, list)


class Binder:
    def __init__(self, data: dict) -> None:
        self._data = data

    def bind(self, bind_type: Type) -> Any:
        binded = (self._bind_anno.origin)()
        self._bind_anno = ClassAnnotation(bind_type)
        for key, prop_anno in self._bind_anno.properties.items():
            if not prop_anno.is_optional and key not in self._data:
                raise TypeError()

            candidate_types = [
                value_type
                for value_type in self._analyze_value_types(self._data, key)
                if value_type in prop_anno.types
            ]
            if len(candidate_types) == 0:
                raise TypeError()

            setattr(binded, key, self._cast_value(prop_anno, self._data, key))

        return binded

    def _analyze_value_types(self, data: dict, key: str) -> List[Type]:
        if key not in data:
            return [type(None)]

        value = data[key]
        if type(value) is int:
            return [int]
        elif type(value) is float:
            return [float]
        elif type(value) is bool:
            return [bool]
        elif type(value) is str and re.search(r'^\d+$', value):
            return [str, int]
        elif type(value) is str and re.search(r'^\d+(\.\d*)?$', value):
            return [str, float]
        elif type(value) is str and value in ['true', 'false']:
            return [str, bool]
        elif type(value) is str:
            return [str]
        elif type(value) is list:
            return [list]
        elif type(value) is dict:
            return [dict]
        else:
            return []

    def _cast_value(self, cast_anno: PropertyAnnotation, data: dict, key: str) -> Any:
        if key not in data:
            return None

        value = data[key]
        if cast_anno.is_enum:
            return (cast_anno.origin)(value)
        elif cast_anno.is_int:
            return int(value)
        elif cast_anno.is_float:
            return float(value)
        elif cast_anno.is_bool:
            return value in ['true', 'false']
        else:
            return value


def pluck(self, node: Node, path: str) -> Node:
    if type(node) is dict and path:
        key, *remain = path.split('.')
        return self._pluck(node[key], '.'.join(remain))
    elif type(node) is list and path:
        key, *remain = path.split('.')
        index = int(key)
        return self._pluck(node[index], '.'.join(remain))
    else:
        return node
