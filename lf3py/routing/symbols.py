from abc import ABCMeta, abstractmethod
from typing import List, Tuple

from lf3py.lang.dsn import DSNElement
from lf3py.lang.locator import Locator
from lf3py.routing.types import AttachMiddleware, Middleware, RunnerDecorator
from lf3py.task import Catch, Task
from lf3py.task.data import Command


class IDispatcher(metaclass=ABCMeta):
    @abstractmethod
    def tasks(self, locator: Locator) -> List[Task]:
        raise NotImplementedError()

    @abstractmethod
    def catches(self, locator: Locator) -> List[Catch]:
        raise NotImplementedError()


class IRouter(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, *spec_elems: DSNElement) -> RunnerDecorator:
        raise NotImplementedError()

    @abstractmethod
    def overlap(self, *attaches: AttachMiddleware) -> RunnerDecorator:
        raise NotImplementedError()

    @abstractmethod
    def register(self, spec: str, *middlewares: Middleware) -> Tuple[str, Middleware]:
        raise NotImplementedError()

    @abstractmethod
    def resolve(self, *elems: DSNElement) -> Tuple[str, List[Middleware]]:
        raise NotImplementedError()

    @abstractmethod
    def dispatch(self, command: Command) -> IDispatcher:
        raise NotImplementedError()
