from abc import ABCMeta, abstractmethod
from typing import Any


class Serializer(metaclass=ABCMeta):
    @abstractmethod
    def serialize(self, any: Any) -> Any:
        raise NotImplementedError()


class DictSerializer(Serializer):
    def serialize(self, any: Any) -> dict:
        return any.__dict__
