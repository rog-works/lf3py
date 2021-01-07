from typing_extensions import Protocol

from lf3py.api.symbols import IApiRouter, IApiSchema
from lf3py.routing.symbols import IRouter
from lf3py.routing.types import AttachMiddleware, CatchMiddleware, RunnerDecorator


class Blueprint(Protocol):
    def behavior(self, *attaches: AttachMiddleware) -> RunnerDecorator:
        raise NotImplementedError()

    def on_error(self, *catches: CatchMiddleware) -> RunnerDecorator:
        raise NotImplementedError()

    @property
    def route(self) -> IRouter:
        raise NotImplementedError()


class ApiBlueprint(Protocol):
    def behavior(self, *attaches: AttachMiddleware) -> RunnerDecorator:
        raise NotImplementedError()

    def on_error(self, *catches: CatchMiddleware) -> RunnerDecorator:
        raise NotImplementedError()

    @property
    def api(self) -> IApiRouter:
        raise NotImplementedError()

    @property
    def schema(self) -> IApiSchema:
        raise NotImplementedError()
