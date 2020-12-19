from lf3py.api.request import Request
from lf3py.api.routers.api import IApiRouter
from lf3py.api.routers.args import resolve_args
from lf3py.api.routers.dsn import RouteDSN
from lf3py.lang.module import load_module_path
from lf3py.task.result import Result
from lf3py.task.router import Router, Routes
from lf3py.task.types import DSNType, Runner, RunnerDecorator


class BpRouter(Router, IApiRouter):
    def __init__(self, request: Request, routes: Routes, dsn_type: DSNType = RouteDSN) -> None:
        super(BpRouter, self).__init__(dsn_type, routes)
        self._request = request

    def __call__(self, method: str, path_spec: str) -> RunnerDecorator:
        def decorator(runner: Runner) -> Runner:
            self.register(runner, method, path_spec)

            def wrapper(*args, **kwargs) -> Result:
                dsn = self.dsnize(self._request.method, self._request.path)
                path_params = dsn.capture(dsn.format(method, path_spec))
                inject_args = resolve_args(runner, path_params, self._request.params)
                if type(inject_args) is tuple:
                    return runner(inject_args[0], **inject_args[1])
                else:
                    return runner(**inject_args)

            return wrapper

        return decorator

    def dispatch(self, request: Request) -> Runner:
        _, module_path = self.resolve(request.method, request.path)
        runner = load_module_path(module_path)
        return runner()
