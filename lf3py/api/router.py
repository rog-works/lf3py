from lf3py.api.request import Request
from lf3py.api.symbols import IApiRouter
from lf3py.routing.routers.types import IRouter
from lf3py.task.data import Result
from lf3py.task.types import RunnerDecorator


class ApiRouter(IApiRouter):
    def __init__(self, router: IRouter) -> None:
        self._router = router

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

    def dispatch(self, request: Request) -> Result:
        return self._router.dispatch(request)
