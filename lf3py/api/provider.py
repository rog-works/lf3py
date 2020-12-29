from lf3py.api.dsn import ApiDSN
from lf3py.api.request import Request
from lf3py.api.router import ApiRouter
from lf3py.aws.api.decode import decode_request
from lf3py.aws.types import LambdaEvent
from lf3py.config.types import Routes
from lf3py.routing.routers.bp import BpRouter
from lf3py.routing.routers.flow import FlowRouter
from lf3py.routing.routers.root import RootRouter
from lf3py.routing.routers.types import IRouter
from lf3py.session.session import Session


def api_router(session: Session) -> ApiRouter:
    return ApiRouter(RootRouter(session))


def bp_router(request: Request, routes: Routes) -> IRouter:
    return BpRouter(request, routes)


def flow_router() -> IRouter:
    return FlowRouter(ApiDSN)


def request(event: LambdaEvent) -> Request:
    decoded = decode_request(event)
    return Request(
        path=decoded['path'],
        method=decoded['method'],
        headers=decoded['headers'],
        params=decoded['params'],
    )
