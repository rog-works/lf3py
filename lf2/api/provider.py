from lf2.api.dsn import RouteDSN
from lf2.api.request import Request
from lf2.api.route import Route
from lf2.task.router import Router, Routes
from lf2.task.runner import Runner


def bp_router(routes: Routes) -> Router:
    return Router(RouteDSN, routes)


def api_router() -> Router:
    return Router(RouteDSN)


def runner(request: Request, route: Route) -> Runner:
    return route.resolve(request)
