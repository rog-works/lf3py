from abc import ABCMeta

from lf3py.lang.dsn import DSNElement
from lf3py.task.data import Command, Result
from lf3py.task.types import RunnerDecorator


class IRouter(metaclass=ABCMeta):
    def __call__(self, *spec_elems: DSNElement) -> RunnerDecorator:
        raise NotImplementedError()

    def dispatch(self, command: Command) -> Result:
        raise NotImplementedError()
