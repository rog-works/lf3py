from typing import Dict, Tuple

from lf3py.config import Routes
from lf3py.lang.dsn import DSN, DSNElement, DSNType
from lf3py.lang.module import load_module_path
from lf3py.routing.errors import RouteMismatchError
from lf3py.routing.invoker import invoke
from lf3py.routing.symbols import IRouter
from lf3py.task import Task
from lf3py.task.data import Command
from lf3py.task.types import Runner, RunnerDecorator


class Router(IRouter):
    def __init__(self, dsn_type: DSNType, routes: Routes = Routes()) -> None:
        self._dsn_type = dsn_type
        self._routes = routes

    def __call__(self, *spec_elems: DSNElement) -> RunnerDecorator:
        def decorator(runner: Runner) -> Runner:
            self.register(runner, *spec_elems)
            return runner

        return decorator

    def register(self, runner: Runner, *elems: DSNElement):
        spec = self._dsn_type.format(*elems)
        self._routes[spec] = f'{runner.__module__}.{runner.__name__}'

    def _resolve_spec_path(self, *elems: DSNElement) -> Tuple[str, str]:
        dsn = self.dsnize(*elems)
        for spec, module_path in self._routes.items():
            if dsn.contains(spec):
                return spec, module_path

        raise RouteMismatchError(f'Missing route. route = {dsn}')

    def dsnize(self, *elems: DSNElement) -> DSN:
        return self._dsn_type(*elems)

    def dispatch(self, command: Command) -> Task:
        spec, runner = self.resolve(command.dsn.to_str())
        return Task(runner, lambda: invoke(runner, command, spec))


class BpRouter(Router):
    def __init__(self, dsn_type: DSNType, routes: Routes) -> None:
        super(BpRouter, self).__init__(dsn_type, routes)

    def resolve(self, *elems: DSNElement) -> Tuple[str, Runner]:
        spec, module_path = self._resolve_spec_path(*elems)
        return spec, load_module_path(module_path)


class InlineRouter(Router):
    def __init__(self, dsn_type: DSNType = DSN) -> None:
        super(InlineRouter, self).__init__(dsn_type)
        self._runners: Dict[str, Runner] = {}

    def register(self, runner: Runner, *elems: DSNElement):
        super(InlineRouter, self).register(runner, *elems)
        spec = self._dsn_type.format(*elems)
        self._runners[spec] = runner

    def resolve(self, *elems: DSNElement) -> Tuple[str, Runner]:
        spec, _ = self._resolve_spec_path(*elems)
        return spec, self._runners[spec]
