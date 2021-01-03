from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Any, Type, TypeVar

from lf3py.lang.dsn import DSN
from lf3py.serialization.serializer import DictSerializer, Serializer

T_OBJ = TypeVar('T_OBJ')


class Command(metaclass=ABCMeta):
    @property
    @abstractmethod
    def dsn(self) -> DSN:
        raise NotImplementedError()

    @abstractmethod
    def data(self, data_type: Type[T_OBJ]) -> T_OBJ:
        raise NotImplementedError()


@dataclass
class Result:
    _serializer: Serializer = DictSerializer()

    def serialize(self) -> Any:
        return self._serializer.serialize(self)


Ok = Result()
