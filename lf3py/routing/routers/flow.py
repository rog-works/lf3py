from typing import Optional

from lf3py.lang.dsn import DSNElement, DSNType
from lf3py.routing.args import resolve_args
from lf3py.routing.errors import UnexpectedDispatchError
from lf3py.routing.routers import Router
from lf3py.task.data import Command, Result
from lf3py.task.types import Runner, RunnerDecorator


class FlowRouter(Router):
    def __init__(self, dsn_type: DSNType) -> None:
        super(FlowRouter, self).__init__(dsn_type)
        self._command: Optional[Command] = None

    def __call__(self, *spec_elems: DSNElement) -> RunnerDecorator:
        def decorator(runner: Runner) -> Runner:
            self.register(runner, *spec_elems)

            def wrapper(*args, **kwargs) -> Result:
                if self._command is None:
                    raise UnexpectedDispatchError('Command is None')

                spec = self._command.dsn.format(*spec_elems)
                inject_args = resolve_args(runner, self._command, spec)
                if type(inject_args) is tuple:
                    return runner(inject_args[0], **inject_args[1])
                else:
                    return runner(**inject_args)

            return wrapper

        return decorator

    def dispatch(self, command: Command) -> Result:
        self._command = command
        return super(FlowRouter, self).dispatch(command)
