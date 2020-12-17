from lf2.api.errors import BadRequestError
from lf2.api.request import Request
from lf2.lang.annotation import FunctionAnnotation
from lf2.lang.error import raises
from lf2.serialization.deserializer import DictDeserializer
from lf2.serialization.errors import DeserializeError
from lf2.task.result import Result
from lf2.task.router import Router
from lf2.task.runner import Runner, RunnerDecorator


class ApiRoute:
    def __init__(self, request: Request, router: Router) -> None:
        self._request = request
        self._router = router

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
        def decorator(runner: Runner) -> Runner:
            self._router.register(runner, method, path_spec)

            def wrapper(*args, **kwargs) -> Result:
                dsn = self._router.dsnize(self._request.method, self._request.path)
                path_params = dsn.capture(dsn.format(method, path_spec))
                return self.__invoke(runner, path_params, self._request.params)

            return wrapper

        return decorator

    @raises(BadRequestError, DeserializeError, KeyError, ValueError)
    def __invoke(self, runner: Runner, path_params: dict, params: dict) -> Result:
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
            return runner(func_anno.receiver, **inject_kwargs)
        else:
            return runner(**inject_kwargs)
