from abc import ABCMeta
from dataclasses import dataclass
from typing import Any, Type, TypeVar

from lf3py.lang.dsn import DSN
from lf3py.serialization.serializer import DictSerializer, Serializer

_T = TypeVar('_T')


class Command(metaclass=ABCMeta):
    @property
    def dsn(self) -> DSN:
        raise NotImplementedError()

    def data(self, data_type: Type[_T]) -> _T:
        raise NotImplementedError()


@dataclass
class Result:
    _serializer: Serializer = DictSerializer()

    def serialize(self) -> Any:
        return self._serializer.serialize(self)
