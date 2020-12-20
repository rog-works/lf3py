from typing import Callable, Tuple

from lf3py.config import Routes
from lf3py.lang.dsn import DSN, DSNElement, DSNType
from lf3py.task.data import Command, Result
from lf3py.task.types import RunnerDecorator


class Router:
    def __init__(self, dsn_type: DSNType, routes: Routes = Routes()) -> None:
        self._dsn_type = dsn_type
        self._routes = routes

    def __call__(self, *spec_elems: DSNElement) -> RunnerDecorator:
        raise NotImplementedError()

    def register(self, func: Callable, *elems: DSNElement):
        spec = self._dsn_type.format(*elems)
        self._routes[spec] = f'{func.__module__}.{func.__name__}'

    def resolve(self, *elems: DSNElement) -> Tuple[str, str]:
        dsn = self.dsnize(*elems)
        for spec, module_path in self._routes.items():
            if dsn.contains(spec):
                return spec, module_path

        raise LookupError(f'Missing route. route = {dsn}')

    def dispatch(self, command: Command) -> Result:
        raise NotImplementedError()

    def dsnize(self, *elems: DSNElement) -> DSN:
        return self._dsn_type(*elems)
