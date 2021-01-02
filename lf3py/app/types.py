from typing_extensions import Protocol

from lf3py.api.router import IApiRouter
from lf3py.routing.symbols import IRouter
from lf3py.middleware.types import AttachMiddleware, CatchMiddleware
from lf3py.task.types import RunnerDecorator


class IBlueprinter(Protocol):
    def behavior(self, *attaches: AttachMiddleware) -> RunnerDecorator:
        raise NotImplementedError()

    def on_error(self, *catches: CatchMiddleware) -> RunnerDecorator:
        raise NotImplementedError()

    @property
    def route(self) -> IRouter:
        raise NotImplementedError()


class IApiBlueprinter(Protocol):
    def behavior(self, *attaches: AttachMiddleware) -> RunnerDecorator:
        raise NotImplementedError()

    def on_error(self, *catches: CatchMiddleware) -> RunnerDecorator:
        raise NotImplementedError()

    @property
    def api(self) -> IApiRouter:
        raise NotImplementedError()
