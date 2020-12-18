from dataclasses import dataclass, field
from typing import Any, Dict

from lf2.aws.decode import decode_request
from lf2.aws.types import LambdaEvent


@dataclass
class Request:
    path: str = ''
    method: str = ''
    headers: Dict[str, str] = field(default_factory=dict)
    params: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_event(cls, event: LambdaEvent) -> 'Request':
        decoded = decode_request(event)
        return cls(
            path=decoded['path'],
            method=decoded['method'],
            headers=decoded['headers'],
            params=decoded['params'],
        )
