from lf3py.api.symbols import IApiSchema
from lf3py.routing.symbols import IRouter
from lf3py.routing.types import AttachMiddleware, CatchMiddleware, RunnerDecorator


class ApiSchema(IApiSchema):
    def __init__(self, router: IRouter) -> None:
        self._router = router

    def consume(self, *attaches: AttachMiddleware) -> RunnerDecorator:
        return self._router.overlap(*attaches)

    def produce(self, *attaches: AttachMiddleware) -> RunnerDecorator:
        return self._router.overlap(*attaches)

    def secutity(self, *attaches: AttachMiddleware) -> RunnerDecorator:
        return self._router.overlap(*attaches)

    def header(self, *attaches: AttachMiddleware) -> RunnerDecorator:
        return self._router.overlap(*attaches)

    def error(self, *catches: CatchMiddleware) -> RunnerDecorator:
        return self._router.overlap(*catches)
