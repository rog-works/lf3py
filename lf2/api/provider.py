from lf2.api.request import Request
from lf2.aws.decode import decode_request
from lf2.aws.types import LambdaEvent


def request(event: LambdaEvent) -> Request:
    decoded = decode_request(event)
    return Request(
        path=decoded['path'],
        method=decoded['method'],
        headers=decoded['headers'],
        params=decoded['params'],
    )
