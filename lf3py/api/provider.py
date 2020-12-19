from lf3py.api.request import Request
from lf3py.aws.decode import decode_request
from lf3py.aws.types import LambdaEvent


def request(event: LambdaEvent) -> Request:
    decoded = decode_request(event)
    return Request(
        path=decoded['path'],
        method=decoded['method'],
        headers=decoded['headers'],
        params=decoded['params'],
    )
