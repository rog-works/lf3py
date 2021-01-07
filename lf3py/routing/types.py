from typing import Callable, Union
from typing_extensions import Protocol

from lf3py.task.data import Result


class CatchMiddleware(Protocol):
    def __call__(self, e: Exception, *services) -> None:
        raise NotImplementedError()


AttachMiddleware = Callable[..., None]
RunnerMiddleware = Callable[..., Result]
Middleware = Union[AttachMiddleware, CatchMiddleware, RunnerMiddleware]
RunnerDecorator = Callable[[RunnerMiddleware], RunnerMiddleware]
