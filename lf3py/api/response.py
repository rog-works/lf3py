from dataclasses import dataclass, field
from typing import Dict, List, TypeVar

from lf3py.task.data import Result

T_RES = TypeVar('T_RES', bound='Response')


@dataclass
class Response(Result):
    statusCode: int = 200
    headers: Dict[str, str] = field(default_factory=dict)
    body: Result = Result()

    def json(self: T_RES) -> T_RES:
        self.headers['Content-Type'] = 'application/json'
        return self

    def html(self: T_RES) -> T_RES:
        self.headers['Content-Type'] = 'text/html'
        return self

    def text(self: T_RES) -> T_RES:
        self.headers['Content-Type'] = 'text/plain'
        return self


@dataclass
class MessageBody(Result):
    message: str = ''


@dataclass
class ErrorBody(Result):
    message: str = ''
    stacktrace: List[str] = field(default_factory=list)
