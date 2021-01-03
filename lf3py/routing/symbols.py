from abc import ABCMeta, abstractmethod
from typing import Tuple

from lf3py.lang.dsn import DSNElement
from lf3py.task import Task
from lf3py.task.data import Command
from lf3py.task.types import Runner, RunnerDecorator


class IRouter(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, *spec_elems: DSNElement) -> RunnerDecorator:
        raise NotImplementedError()

    @abstractmethod
    def resolve(self, *elems: DSNElement) -> Tuple[str, Runner]:
        raise NotImplementedError()

    @abstractmethod
    def dispatch(self, command: Command) -> Task:
        raise NotImplementedError()
