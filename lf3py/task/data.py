from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Any, List, Type, TypeVar

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


class CommandQueue:
    def __init__(self) -> None:
        self._queue: List[Command] = []

    @property
    def has_next(self) -> bool:
        return len(self._queue) > 0

    def enqueue(self, *commands: Command):
        self._queue.extend(commands)

    def __iter__(self) -> 'CommandQueue':
        return self

    def __next__(self) -> Command:
        if not self.has_next:
            raise StopIteration()

        task = self._queue[0]
        self._queue = self._queue[1:]
        return task


@dataclass
class Result:
    _serializer: Serializer = DictSerializer()

    def serialize(self) -> Any:
        return self._serializer.serialize(self)


Ok = Result()
