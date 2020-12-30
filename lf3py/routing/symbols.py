from abc import ABCMeta
from typing import Tuple

from lf3py.lang.dsn import DSNElement
from lf3py.task.data import Command, Result
from lf3py.task.types import RunnerDecorator


class IRouter(metaclass=ABCMeta):
    def __call__(self, *spec_elems: DSNElement) -> RunnerDecorator:
        raise NotImplementedError()

    def resolve(self, *spec_elems: DSNElement) -> Tuple[str, str]:
        raise NotImplementedError()


class IDispatcher(metaclass=ABCMeta):
    def dispatch(self, command: Command, router: IRouter) -> Result:
        raise NotImplementedError()
