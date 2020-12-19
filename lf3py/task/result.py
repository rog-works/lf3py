from dataclasses import dataclass
from typing import Any

from lf3py.serialization.serializer import DictSerializer, Serializer


@dataclass
class Result:
    _serializer: Serializer = DictSerializer()

    def serialize(self) -> Any:
        return self._serializer.serialize(self)
