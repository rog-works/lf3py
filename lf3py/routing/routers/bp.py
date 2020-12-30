from lf3py.config import Routes
from lf3py.lang.dsn import DSNElement, DSNType
from lf3py.routing.routers import Router
from lf3py.task.types import Runner, RunnerDecorator


class BpRouter(Router):
    def __init__(self, dsn_type: DSNType, routes: Routes) -> None:
        super(BpRouter, self).__init__(dsn_type, routes)

    def __call__(self, *spec_elems: DSNElement) -> RunnerDecorator:
        def decorator(runner: Runner) -> Runner:
            return runner

        return decorator
