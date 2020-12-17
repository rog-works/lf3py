from lf2.api.path import PathDSN
from lf2.api.request import Request
from lf2.lang.module import load_module_path
from lf2.task.router import Router, Routes
from lf2.task.runner import Runner


def api_router(routes: Routes) -> Router:
    return Router(PathDSN, routes)


def runner(request: Request, router: Router) -> Runner:
    _, module_path = router.resolve(request.method, request.path)
    return load_module_path(module_path)
