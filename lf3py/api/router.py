from lf3py.api.dsn import ApiDSN
from lf3py.api.symbols import IApiRouter
from lf3py.config.types import Routes
from lf3py.routing.router import BpRouter, FlowRouter
from lf3py.task.types import RunnerDecorator


class ImplApiRouter(IApiRouter):
    def get(self, path_spec: str) -> RunnerDecorator:
        return self('GET', path_spec)

    def post(self, path_spec: str) -> RunnerDecorator:
        return self('POST', path_spec)

    def put(self, path_spec: str) -> RunnerDecorator:
        return self('PUT', path_spec)

    def delete(self, path_spec: str) -> RunnerDecorator:
        return self('DELETE', path_spec)

    def patch(self, path_spec: str) -> RunnerDecorator:
        return self('PATCH', path_spec)

    def option(self, path_spec: str) -> RunnerDecorator:
        return self('OPTION', path_spec)

    def head(self, path_spec: str) -> RunnerDecorator:
        return self('HEAD', path_spec)


class BpApiRouter(BpRouter, ImplApiRouter):
    def __init__(self, routes: Routes) -> None:
        super(BpApiRouter, self).__init__(ApiDSN, routes)


class FlowApiRouter(FlowRouter, ImplApiRouter):
    def __init__(self) -> None:
        super(FlowApiRouter, self).__init__(ApiDSN)
