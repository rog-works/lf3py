from typing import Dict

from lf3py.lang.dsn import DSNElement, DSNType
from lf3py.lang.module import load_module_path
from lf3py.routing.args import resolve_args
from lf3py.routing.routers import Router
from lf3py.task.data import Command, Result
from lf3py.task.types import Runner, RunnerDecorator


class FlowRouter(Router):
    def __init__(self, dsn_type: DSNType) -> None:
        super(FlowRouter, self).__init__(dsn_type)
        self._org_runners: Dict[str, Runner] = {}

    def __call__(self, *spec_elems: DSNElement) -> RunnerDecorator:
        def decorator(runner: Runner) -> Runner:
            self.register(runner, *spec_elems)
            module_path = f'{runner.__module__}.{runner.__name__}'
            self._org_runners[module_path] = runner
            return runner

        return decorator

    def dispatch(self, command: Command) -> Result:
        spec, module_path = self.resolve(str(command.dsn))
        runner = load_module_path(module_path)
        org_runner = self._org_runners[module_path]
        inject_args = resolve_args(org_runner, command, spec)
        if type(inject_args) is tuple:
            return runner(inject_args[0], **inject_args[1])
        else:
            return runner(**inject_args)
