from typing import Any

from framework.lang.serialize import DictSerializer, Serializer


class Result:
    serializer: Serializer = DictSerializer()

    def serialize(self) -> Any:
        return self.serializer.serialize(self)
