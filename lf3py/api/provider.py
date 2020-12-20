from lf3py.api.dsn import ApiDSN
from lf3py.api.request import Request
from lf3py.aws.decode import decode_request
from lf3py.aws.types import LambdaEvent
from lf3py.lang.dsn import DSNType


def api_dsn_type() -> DSNType:
    return ApiDSN


def request(event: LambdaEvent) -> Request:
    decoded = decode_request(event)
    return Request(
        path=decoded['path'],
        method=decoded['method'],
        headers=decoded['headers'],
        params=decoded['params'],
    )
