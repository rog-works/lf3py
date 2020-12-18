from lf2.api.path import PathDSN
from lf2.api.request import Request
from lf2.api.route import Route
from lf2.task.router import Router, Routes
from lf2.task.runner import Runner


def bp_router(routes: Routes) -> Router:
    return Router(PathDSN, routes)


def api_router() -> Router:
    return Router(PathDSN)


def runner(request: Request, route: Route) -> Runner:
    return route.resolve(request)
