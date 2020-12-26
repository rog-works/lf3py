from lf3py.api.dsn import ApiDSN
from lf3py.api.request import Request
from lf3py.aws.decode import decode_request
from lf3py.aws.types import LambdaEvent
from lf3py.config.types import Routes
from lf3py.routing.routers.bp import BpRouter
from lf3py.routing.routers.flow import FlowRouter


def bp_router(request: Request, routes: Routes) -> BpRouter:
    return BpRouter(request, routes)


def flow_router() -> FlowRouter:
    return FlowRouter(ApiDSN)


def request(event: LambdaEvent) -> Request:
    decoded = decode_request(event)
    return Request(
        path=decoded['path'],
        method=decoded['method'],
        headers=decoded['headers'],
        params=decoded['params'],
    )
