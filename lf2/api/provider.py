from lf2.api.data import Request
from lf2.api.path import PathDSN
from lf2.task.router import Router, Routes
from lf2.task.runner import Runner


def api_router(routes: Routes) -> Router:
    return Router(PathDSN, routes)


def runner(request: Request, router: Router) -> Runner:
    return router.resolve(request.method, request.path)
