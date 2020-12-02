from dataclasses import dataclass, field
from typing import Any, Dict, List

from framework.task.result import Result


@dataclass
class Request:
    path: str = ''
    method: str = ''
    headers: Dict[str, str] = field(default_factory=dict)
    params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Response(Result):
    status: int = 200
    headers: Dict[str, str] = field(default_factory=dict)
    body: Result = Result()


@dataclass
class ErrorBody(Result):
    message: str = ''
    stacktrace: List[str] = field(default_factory=list)
