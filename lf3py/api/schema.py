from lf3py.api.symbols import IApiSchema
from lf3py.middleware import Middleware
from lf3py.middleware.types import AttachMiddleware, CatchMiddleware
from lf3py.task.types import RunnerDecorator


class ApiSchema(IApiSchema):
    def __init__(self, middleware: Middleware) -> None:
        self._middleware = middleware

    def consume(self, *attaches: AttachMiddleware) -> RunnerDecorator:
        return self._middleware.attach(*attaches)

    def produce(self, *attaches: AttachMiddleware) -> RunnerDecorator:
        return self._middleware.attach(*attaches)

    def secutity(self, *attaches: AttachMiddleware) -> RunnerDecorator:
        return self._middleware.attach(*attaches)

    def header(self, *attaches: AttachMiddleware) -> RunnerDecorator:
        return self._middleware.attach(*attaches)

    def error(self, *catches: CatchMiddleware) -> RunnerDecorator:
        return self._middleware.catch(*catches)
