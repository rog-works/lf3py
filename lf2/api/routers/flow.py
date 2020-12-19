from typing import Dict

from lf2.api.request import Request
from lf2.api.routers.api import IApiRouter
from lf2.api.routers.args import resolve_args
from lf2.api.routers.dsn import RouteDSN
from lf2.lang.module import load_module_path
from lf2.task.result import Result
from lf2.task.router import Router
from lf2.task.types import DSNType, Runner, RunnerDecorator


class FlowRouter(Router, IApiRouter):
    def __init__(self, dsn_type: DSNType = RouteDSN) -> None:
        super(FlowRouter, self).__init__(dsn_type)
        self._org_runners: Dict[str, Runner] = {}

    def __call__(self, method: str, path_spec: str) -> RunnerDecorator:
        def decorator(runner: Runner) -> Runner:
            self.register(runner, method, path_spec)
            module_path = f'{runner.__module__}.{runner.__name__}'
            self._org_runners[module_path] = runner
            return runner

        return decorator

    def dispatch(self, request: Request) -> Result:
        spec, module_path = self.resolve(request.method, request.path)
        dsn = self.dsnize(request.method, request.path)
        path_params = dsn.capture(spec)
        runner = load_module_path(module_path)
        org_runner = self._org_runners[module_path]
        inject_args = resolve_args(org_runner, path_params, request.params)
        if type(inject_args) is tuple:
            return runner(inject_args[0], **inject_args[1])
        else:
            return runner(**inject_args)
