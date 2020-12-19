from lf2.api.request import Request
from lf2.api.routers.dsn import RouteDSN
from lf2.aws.types import LambdaEvent
from lf2.task.router import Router, Routes


def request(event: LambdaEvent) -> Request:
    return Request.from_event(event)


def bp_router(routes: Routes) -> Router:
    return Router(RouteDSN, routes)


def api_router() -> Router:
    return Router(RouteDSN)
