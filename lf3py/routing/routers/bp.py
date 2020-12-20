from lf3py.config import Routes
from lf3py.lang.dsn import DSNElement
from lf3py.lang.module import load_module_path
from lf3py.routing.args import resolve_args
from lf3py.routing.routers import Router
from lf3py.task.data import Command, Result
from lf3py.task.types import Runner, RunnerDecorator


class BpRouter(Router):
    def __init__(self, command: Command, routes: Routes) -> None:
        super(BpRouter, self).__init__(type(command.dsn), routes)
        self._command = command

    def __call__(self, *spec_elems: DSNElement) -> RunnerDecorator:
        def decorator(runner: Runner) -> Runner:
            def wrapper(*args, **kwargs) -> Result:
                spec = self._command.dsn.format(*spec_elems)
                inject_args = resolve_args(runner, self._command, spec)
                if type(inject_args) is tuple:
                    return runner(inject_args[0], **inject_args[1])
                else:
                    return runner(**inject_args)

            return wrapper

        return decorator

    def dispatch(self, command: Command) -> Runner:
        _, module_path = self.resolve(str(command.dsn))
        runner = load_module_path(module_path)
        return runner()
