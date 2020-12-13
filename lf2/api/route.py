from lf2.api.data import Request
from lf2.api.errors import BadRequestError
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
            >>>     return app.ok(body=IndexBody(Model.find_all()))

            >>> @app.route('GET', '/models/{id}')
            >>> def show(id: int) -> Response:
            >>>     return app.ok(body=ShowBody(Model.find(id)))

            >>> @app.route('POST', '/models')
            >>> def create(params: CreateParams) -> Response:
            >>>     return app.ok(body=ShowBody(Model.create(params)))

            >>> @app.route('DELETE', '/models/{id}')
            >>> def delete(id: int) -> Response:
            >>>     Models.find(id).delete()
            >>>     return app.ok()
        """
        def decorator(runner: Runner) -> Runner:
            self._router.register(runner, method, path_spec)

            @raises(BadRequestError, DeserializeError, KeyError, ValueError)
            def wrapper(*args, **kwargs) -> Result:
                dsn = self._router.dsnize(self._request.method, self._request.path)
                func_anno = FunctionAnnotation(runner)

                path_args = dsn.capture(dsn.format(method, path_spec))
                path_args = {
                    key: int(path_args[key]) if arg_anno.origin is int else path_args[key]
                    for key, arg_anno in func_anno.args.items()
                    if key in path_args
                }

                deserializer = DictDeserializer()
                body_args = {
                    key: deserializer.deserialize(arg_anno.origin, self._request.params)
                    for key, arg_anno in func_anno.args.items()
                    if key not in path_args
                }

                inject_kwargs = {**path_args, **body_args}
                if func_anno.is_method:
                    return runner(*(args[0]), **inject_kwargs)
                else:
                    return runner(**inject_kwargs)

            return wrapper

        return decorator
