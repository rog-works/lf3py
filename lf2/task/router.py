from typing import Callable, Dict, Type

from lf2.lang.dsn import DSN, DSNElement
from lf2.lang.module import load_module_path
from lf2.task.runner import Runner, RunnerDecorator


class Routes(Dict[str, str]):
    pass


class Router:
    def __init__(self, dsn_type: Type[DSN], routes: Routes = Routes()) -> None:
        self._dsn_type = dsn_type
        self._routes = routes

    def register(self, func: Callable, *elems: DSNElement):
        spec = self._dsn_type.format(*elems)
        self._routes[spec] = f'{func.__module__}.{func.__name__}'

    def resolve(self, *elems: DSNElement) -> Runner:
        return load_module_path(self.resolve_module_path(*elems))

    def resolve_module_path(self, *elems: DSNElement) -> str:
        dsn = self.dsnize(*elems)
        for spec, module_path in self._routes.items():
            if dsn.like(spec):
                return module_path

        raise ModuleNotFoundError(f'Missing route. route = {dsn}')

    def dsnize(self, *elems: DSNElement) -> DSN:
        return self._dsn_type(*elems)

    def route(self, *elems: DSNElement) -> RunnerDecorator:
        def decorator(func: Runner) -> Runner:
            self.register(func, *elems)
            return func

        return decorator
