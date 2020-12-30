from typing import Tuple

from lf3py.api.symbols import IApiRouter
from lf3py.lang.dsn import DSNElement
from lf3py.routing.symbols import IRouter
from lf3py.task.types import RunnerDecorator


class ApiRouter(IApiRouter):
    def __init__(self, router: IRouter) -> None:
        self._router = router

    def __call__(self, *elems: DSNElement) -> RunnerDecorator:
        return self._router(*elems)

    def resolve(self, *elems: DSNElement) -> Tuple[str, str]:
        return self._router.resolve(*elems)

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
