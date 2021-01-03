from types import ModuleType
from typing import Any, Dict, List, Optional, Tuple
from typing_extensions import Protocol

from lf3py.app.app import App
from lf3py.lang.dict import deep_merge
from lf3py.lang.module import import_module
from lf3py.lang.sequence import first, flatten, last
from lf3py.middleware import Middleware
from lf3py.routing.symbols import IRouter
from lf3py.task.types import Runner


class Generator(Protocol):
    def generate(self, bps: List[App]) -> Any:
        raise NotImplementedError()


class Discovery:
    def __init__(self, filepaths: List[str]) -> None:
        self._bps = self.__discover(list(filepaths))

    def __discover(self, filepaths: List[str]) -> List[App]:
        paths = [self.__to_module_path(filepath) for filepath in filepaths]
        searched = [self.__dirty_resolve_bp(path) for path in paths]
        return [result for result in searched if result]

    def __to_module_path(self, filepath: str) -> str:
        return '.'.join('.'.join(filepath.split('.')[:-1]).split('/'))

    def __dirty_resolve_bp(self, path: str) -> Optional[App]:
        modules = import_module(path)
        for module in modules.__dict__.values():
            if hasattr(module, 'locate') and callable(module.locate) and hasattr(module.locate, '__self__'):
                return module

        return None

    def generate(self, generator: 'Generator') -> Any:
        return generator.generate(self._bps)


class RoutesGenerator:
    def generate(self, bps: List[App]) -> dict:
        return dict(flatten([self.__dirty_get_routes_to_tuple(bp) for bp in bps]))

    def __dirty_get_routes_to_tuple(self, bp: App) -> List[Tuple[str, str]]:
        routes = bp.locate(IRouter)._routes  # FIXME dirty get routes
        return [(dsn_spec, module_path) for dsn_spec, module_path in routes.items()]


class OpenApiGenerator:
    def generate(self, bps: List[App]) -> dict:
        schema = {}
        for bp in bps:
            schema = {**schema, **self.__gen_schema_from_bp(bp)}

        return schema

    def __gen_schema_from_bp(self, bp: App) -> dict:
        middleware = bp.locate(Middleware)
        routes = bp.locate(IRouter)._routes  # FIXME dirty get routes
        path = '.'.join(first(routes.values()).split('.')[:-1])
        modules = import_module(path)
        schema = {'paths': {}}
        for spec, runner in self.__extract_runners(routes, modules).items():
            schema['paths'] = deep_merge(schema['paths'], self.__gen_api_schema(spec, runner, middleware))

        return schema

    def __extract_runners(self, routes: dict, modules: ModuleType) -> Dict[str, Runner]:
        extracted = {}
        for spec, module_path in routes.items():
            module_name = last(module_path.split('.'))
            extracted[spec] = modules.__dict__[module_name]

        return extracted

    def __gen_api_schema(self, spec: str, runner: Runner, middleware: Middleware) -> dict:
        api_schema = self.__gen_api_schema_from_middleware(middleware, runner)
        return self.__gen_api_schema_from_runner(spec, runner, api_schema)

    def __gen_api_schema_from_middleware(self, middleware: Middleware, runner: Runner) -> dict:
        attaches, caches = middleware._attaches.get(runner, []), middleware._catches.get(runner, [])
        elems = flatten([attaches, caches])
        schema = {}
        for elem in elems:
            if hasattr(elem, '__openapi__'):
                schema = deep_merge(schema, getattr(elem, '__openapi__'))

        return schema

    def __gen_api_schema_from_runner(self, spec: str, runner: Runner, api_schema: dict) -> dict:
        method, path = spec.split(' ')
        base_api_schema = {
            'responses': {
                200: {'description': '200 OK'},
            }
        }
        return {
            path: {
                method.lower(): deep_merge(api_schema, base_api_schema)
            }
        }
