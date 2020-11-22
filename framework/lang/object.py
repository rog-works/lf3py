from typing import Any, Type

from framework.lang.annotation import ClassAnnotation, PropertyAnnotation


class Assigner:
    @classmethod
    def assign(cls, assign_type: Type, data: dict) -> Any:
        assign_anno = ClassAnnotation(assign_type)
        assigned = (assign_anno.origin)()
        for key, prop_anno in assign_anno.properties.items():
            if not prop_anno.is_optional and key not in data:
                raise ValueError(f'"{key}" is required key. from {assign_type}')

            setattr(assigned, key, cls._cast_value(prop_anno, data, key))

        return assigned

    @classmethod
    def _cast_value(cls, prop_anno: PropertyAnnotation, data: dict, key: str) -> Any:
        if key not in data:
            return None

        value = data[key]
        if prop_anno.is_enum:
            return (prop_anno.origin)(value)
        elif prop_anno.is_int:
            return int(value)
        elif prop_anno.is_float:
            return float(value)
        elif prop_anno.is_bool:
            return value in ['true', 'false']
        else:
            return value
