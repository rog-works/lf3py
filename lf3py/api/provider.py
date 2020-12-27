from lf3py.api.dsn import ApiDSN
from lf3py.api.request import Request
from lf3py.api.router import ApiRouter
from lf3py.aws.decode import decode_request
from lf3py.aws.types import LambdaEvent
from lf3py.config.types import Routes
from lf3py.routing.routers.bp import BpRouter
from lf3py.routing.routers.flow import FlowRouter


def api_bp_router(request: Request, routes: Routes) -> ApiRouter:
    return ApiRouter(BpRouter(request, routes))


def api_flow_router() -> ApiRouter:
    return ApiRouter(FlowRouter(ApiDSN))


def request(event: LambdaEvent) -> Request:
    decoded = decode_request(event)
    return Request(
        path=decoded['path'],
        method=decoded['method'],
        headers=decoded['headers'],
        params=decoded['params'],
    )
