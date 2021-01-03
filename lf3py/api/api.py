from lf3py.middleware import Middleware
from lf3py.middleware.types import AttachMiddleware, CatchMiddleware
from lf3py.routing.symbols import IRouter
from lf3py.task.types import RunnerDecorator


class Api:
    def __init__(self, router: IRouter, middleware: Middleware) -> None:
        self._router = router
        self._middleware = middleware

    def get(self, path_spec: str) -> RunnerDecorator:
        return self._router('GET', path_spec)

    def post(self, path_spec: str) -> RunnerDecorator:
        return self._router('POST', path_spec)

    def put(self, path_spec: str) -> RunnerDecorator:
        return self._router('PUT', path_spec)

    def delete(self, path_spec: str) -> RunnerDecorator:
        return self._router('DELETE', path_spec)

    def patch(self, path_spec: str) -> RunnerDecorator:
        return self._router('PATCH', path_spec)

    def option(self, path_spec: str) -> RunnerDecorator:
        return self._router('OPTION', path_spec)

    def head(self, path_spec: str) -> RunnerDecorator:
        return self._router('HEAD', path_spec)

    def consume(self, *attaches: AttachMiddleware) -> RunnerDecorator:
        return self._middleware.attach(*attaches)

    def produce(self, *attaches: AttachMiddleware) -> RunnerDecorator:
        return self._middleware.attach(*attaches)

    def secutity(self, *attaches: AttachMiddleware) -> RunnerDecorator:
        return self._middleware.attach(*attaches)

    def output(self, *catches: CatchMiddleware) -> RunnerDecorator:
        return self._middleware.catch(*catches)
