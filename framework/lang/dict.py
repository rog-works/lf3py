from typing import Any, List, Type
import re

from framework.lang.annotation import ClassAnnotation, PropertyAnnotation


class Binder:
    def __init__(self, bind_type: Type) -> None:
        self._bind_anno = ClassAnnotation(bind_type)

    def bind(self, params: dict) -> Any:
        binded_params = (self._bind_anno.origin)()
        for key, prop_anno in self._bind_anno.properties.items():
            if not prop_anno.is_optional and key not in params:
                raise TypeError()

            candidate_types = [
                value_type
                for value_type in self._analyze_value_types(params, key)
                if value_type in prop_anno.types
            ]
            if len(candidate_types) == 0:
                raise TypeError()

            setattr(binded_params, key, self._cast_value(prop_anno, params, key))

        return binded_params

    def _analyze_value_types(self, params: dict, key: str) -> List[Type]:
        if key not in params:
            return [type(None)]

        value = params[key]
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

    def _cast_value(self, cast_anno: PropertyAnnotation, params: dict, key: str) -> Any:
        if key not in params:
            return None

        value = params[key]
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
