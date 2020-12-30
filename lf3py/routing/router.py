from typing import Dict, Tuple

from lf3py.config import Routes
from lf3py.lang.dsn import DSN, DSNElement, DSNType
from lf3py.routing.errors import RouteMismatchError
from lf3py.routing.symbols import IRouter
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

    def resolve(self, *elems: DSNElement) -> Tuple[str, str]:
        dsn = self.dsnize(*elems)
        for spec, module_path in self._routes.items():
            if dsn.contains(spec):
                return spec, module_path

        raise RouteMismatchError(f'Missing route. route = {dsn}')

    def dsnize(self, *elems: DSNElement) -> DSN:
        return self._dsn_type(*elems)


class BpRouter(Router):
    def __init__(self, dsn_type: DSNType, routes: Routes) -> None:
        super(BpRouter, self).__init__(dsn_type, routes)


class FlowRouter(Router):
    def __init__(self, dsn_type: DSNType = DSN) -> None:
        super(FlowRouter, self).__init__(dsn_type)
        self._runners: Dict[str, Runner] = {}

    def __call__(self, *spec_elems: DSNElement) -> RunnerDecorator:
        def decorator(runner: Runner) -> Runner:
            self.register(runner, *spec_elems)
            spec = self._dsn_type.format(*spec_elems)
            self._runners[spec] = runner
            return runner

        return decorator

    def resolve_runner(self, *elems: DSNElement) -> Tuple[str, Runner]:
        spec, _ = self.resolve(*elems)
        return spec, self._runners[spec]
