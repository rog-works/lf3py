from dataclasses import dataclass, field

from framework.task.result import Result


@dataclass
class Request:
    path: str = ''
    method: str = ''
    headers: dict = field(default_factory=dict)
    params: dict = field(default_factory=dict)


@dataclass
class Response(Result):
    status: int = 200
    headers: dict = field(default_factory=dict)
    body: dict = field(default_factory=dict)
