from typing import Any, Dict

from lf2.aws.decode import decode_request
from lf2.aws.types import LambdaEvent


class Request:
    def __init__(self, event: LambdaEvent) -> None:
        decoded = decode_request(event)
        self.path: str = decoded['path']
        self.method: str = decoded['method']
        self.headers: Dict[str, str] = decoded['headers']
        self.params: Dict[str, Any] = decoded['params']
