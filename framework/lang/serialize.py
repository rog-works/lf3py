from abc import ABCMeta, abstractmethod
from typing import Any


class Serializer(metaclass=ABCMeta):
    @abstractmethod
    def serialize(self, obj: Any) -> Any:
        raise NotImplementedError()


class DictSerializer(Serializer):
    def serialize(self, obj: Any) -> dict:
        return {key: value for key, value in obj.__dict__.items() if not key.startswith('_')}
