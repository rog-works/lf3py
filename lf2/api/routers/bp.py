from lf2.api.request import Request
from lf2.api.routers.api import ApiRouter
from lf2.api.routers.args import resolve_args
from lf2.lang.module import load_module_path
from lf2.task.result import Result
from lf2.task.router import Router
from lf2.task.runner import Runner, RunnerDecorator


class BpRouter(ApiRouter):
    def __init__(self, request: Request, router: Router) -> None:
        self._request = request
        self._router = router

    def __call__(self, method: str, path_spec: str) -> RunnerDecorator:
        def decorator(runner: Runner) -> Runner:
            self._router.register(runner, method, path_spec)

            def wrapper(*args, **kwargs) -> Result:
                dsn = self._router.dsnize(self._request.method, self._request.path)
                path_params = dsn.capture(dsn.format(method, path_spec))
                inject_args = resolve_args(runner, path_params, self._request.params)
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
