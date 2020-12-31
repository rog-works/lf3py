from abc import ABCMeta
from typing import Tuple

from lf3py.lang.dsn import DSNElement
from lf3py.task.data import Command, Result
from lf3py.task.types import Runner, RunnerDecorator


class IRouter(metaclass=ABCMeta):
    def __call__(self, *spec_elems: DSNElement) -> RunnerDecorator:
        raise NotImplementedError()

    def resolve(self, *elems: DSNElement) -> Tuple[str, Runner]:
        raise NotImplementedError()

    def dispatch(self, command: Command) -> Result:
        raise NotImplementedError()
