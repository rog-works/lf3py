from typing import Dict, List, Tuple

from lf3py.config import Routes
from lf3py.lang.dsn import DSN, DSNElement, DSNType
from lf3py.lang.module import import_module
from lf3py.lang.sequence import first
from lf3py.routing.dispatcher import Dispatcher
from lf3py.routing.errors import RouteMismatchError
from lf3py.routing.symbols import IRouter
from lf3py.routing.types import AttachMiddleware, Middleware, RunnerMiddleware, RunnerDecorator
from lf3py.task.data import Command


class Router(IRouter):
    def __init__(self, dsn_type: DSNType = DSN) -> None:
        self._dsn_type = dsn_type
        self._middlewares: Dict[str, List[Middleware]] = {}

    def __call__(self, *spec_elems: DSNElement) -> RunnerDecorator:
        def decorator(runner: RunnerMiddleware) -> RunnerMiddleware:
            self.register(self._dsn_type.format(*spec_elems), runner)
            return runner

        return decorator

    def register(self, spec: str, *middlewares: Middleware):
        if spec not in self._middlewares:
            self._middlewares[spec] = []

        self._middlewares[spec] = [*middlewares, *self._middlewares[spec]]

    def resolve(self, *elems: DSNElement) -> Tuple[str, List[Middleware]]:
        dsn = self.dsnize(*elems)
        for spec, middlewares in self._middlewares.items():
            if dsn.contains(spec):
                return spec, middlewares

        raise RouteMismatchError(f'Missing route. route = {dsn}')

    def overlap(self, *attaches: AttachMiddleware) -> RunnerDecorator:
        def decorator(runner: RunnerMiddleware) -> RunnerMiddleware:
            spec = self._to_dsn_spec(runner)
            self.register(spec, *attaches)
            return runner

        return decorator

    def _to_dsn_spec(self, runner: RunnerMiddleware) -> str:
        return first([spec for spec, middlewares in self._middlewares.items() if runner in middlewares])

    def dsnize(self, *elems: DSNElement) -> DSN:
        return self._dsn_type(*elems)

    def dispatch(self, command: Command) -> Dispatcher:
        return Dispatcher(self, command)


class BpRouter(Router):
    def __init__(self, dsn_type: DSNType, routes: Routes) -> None:
        super(BpRouter, self).__init__(dsn_type)
        self._routes = routes

    def resolve(self, *elems: DSNElement) -> Tuple[str, List[Middleware]]:
        dsn = self.dsnize(*elems)
        for spec, module_path in self._routes.items():
            if dsn.contains(spec):
                return spec, self.__dirty_resolve_middlewares(spec, module_path)

        raise RouteMismatchError(f'Missing route. route = {dsn}')

    def __dirty_resolve_middlewares(self, spec: str, module_path: str) -> List[Middleware]:
        path = '.'.join(module_path.split('.')[:-1])
        modules = import_module(path)
        router = first([
            module.locate(IRouter)
            for module in modules.__dict__.values()
            if hasattr(module, 'locate') and callable(module.locate) and hasattr(module.locate, '__self__')
        ])
        return router._middlewares[spec]


class InlineRouter(Router):
    pass
