from abc import ABCMeta
from typing import Any, Dict, Tuple, Union

from lf2.api.errors import BadRequestError
from lf2.api.request import Request
from lf2.lang.annotation import FunctionAnnotation
from lf2.lang.error import raises
from lf2.lang.module import load_module_path
from lf2.serialization.deserializer import DictDeserializer
from lf2.serialization.errors import DeserializeError
from lf2.task.result import Result
from lf2.task.router import Router
from lf2.task.runner import Runner, RunnerDecorator


class Route(metaclass=ABCMeta):
    def __call__(self, method: str, path_spec: str) -> RunnerDecorator:
        """
        Examples:
            >>> @app.route('GET', '/models')
            >>> def index() -> Response:
            >>>     return app.render.ok(body=IndexBody(Model.find_all()))

            >>> @app.route('GET', '/models/{id}')
            >>> def show(id: int) -> Response:
            >>>     return app.render.ok(body=ShowBody(Model.find(id)))

            >>> @app.route('POST', '/models')
            >>> def create(params: CreateParams) -> Response:
            >>>     return app.render.ok(body=ShowBody(Model.create(params)))

            >>> @app.route('DELETE', '/models/{id}')
            >>> def delete(id: int) -> Response:
            >>>     Models.find(id).delete()
            >>>     return app.render.ok()
        """
        raise NotImplementedError()

    def dispatch(self, request: Request) -> Result:
        raise NotImplementedError()

    @raises(BadRequestError, DeserializeError, KeyError, ValueError)
    def _resolve_args(self, runner: Runner, path_params: dict, params: dict) -> Union[Tuple[Any, dict], dict]:
        func_anno = FunctionAnnotation(runner)

        path_kwargs = {
            key: int(path_params[key]) if arg_anno.origin is int else path_params[key]
            for key, arg_anno in func_anno.args.items()
            if key in path_params
        }

        deserializer = DictDeserializer()
        body_kwargs = {
            key: deserializer.deserialize(arg_anno.origin, params)
            for key, arg_anno in func_anno.args.items()
            if key not in path_kwargs
        }

        inject_kwargs = {**path_kwargs, **body_kwargs}
        if func_anno.is_method:
            return func_anno.receiver, inject_kwargs
        else:
            return inject_kwargs


class BpRoute(Route):
    def __init__(self, request: Request, router: Router) -> None:
        self._request = request
        self._router = router

    def __call__(self, method: str, path_spec: str) -> RunnerDecorator:
        def decorator(runner: Runner) -> Runner:
            self._router.register(runner, method, path_spec)

            def wrapper(*args, **kwargs) -> Result:
                dsn = self._router.dsnize(self._request.method, self._request.path)
                path_params = dsn.capture(dsn.format(method, path_spec))
                inject_args = self._resolve_args(runner, path_params, self._request.params)
                if type(inject_args) is tuple:
                    return runner(inject_args[0], **inject_args[1])
                else:
                    return runner(**inject_args)

            return wrapper

        return decorator

    def dispatch(self, request: Request) -> Runner:
        _, module_path = self._router.resolve(request.method, request.path)
        runner = load_module_path(module_path)
        return runner()


class ApiRoute(Route):
    def __init__(self, router: Router) -> None:
        self._router = router
        self._org_runners: Dict[str, Runner] = {}

    def __call__(self, method: str, path_spec: str) -> RunnerDecorator:
        def decorator(runner: Runner) -> Runner:
            self._router.register(runner, method, path_spec)
            module_path = f'{runner.__module__}.{runner.__name__}'
            self._org_runners[module_path] = runner
            return runner

        return decorator

    def dispatch(self, request: Request) -> Result:
        spec, module_path = self._router.resolve(request.method, request.path)
        dsn = self._router.dsnize(request.method, request.path)
        path_params = dsn.capture(spec)
        runner = load_module_path(module_path)
        org_runner = self._org_runners[module_path]
        inject_args = self._resolve_args(org_runner, path_params, request.params)
        if type(inject_args) is tuple:
            return runner(inject_args[0], **inject_args[1])
        else:
            return runner(**inject_args)
