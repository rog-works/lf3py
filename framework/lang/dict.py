from typing import Any, Type, Union

from framework.lang.annotation import ClassAnnotation, PropertyAnnotation


Node = Union[int, float, str, dict, list]


class Binder:
    def __init__(self, data: dict) -> None:
        self._data = data

    def bind(self, bind_type: Type) -> Any:
        bind_anno = ClassAnnotation(bind_type)
        binded = (bind_anno.origin)()
        for key, prop_anno in bind_anno.properties.items():
            if not prop_anno.is_optional and key not in self._data:
                raise ValueError(f'"{key}" is required key. from {bind_type}')

            setattr(binded, key, self._cast_value(prop_anno, self._data, key))

        return binded

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


def pluck(node: Node, path: str) -> Node:
    if type(node) is dict and path:
        key, *remain = path.split('.')
        return pluck(node[key], '.'.join(remain))
    elif type(node) is list and path:
        key, *remain = path.split('.')
        index = int(key)
        return pluck(node[index], '.'.join(remain))
    else:
        return node
