from dataclasses import dataclass

from framework.task.result import Result


@dataclass
class Request:
    path: str = ''
    method: str = ''
    headers: dict = {}
    params: dict = {}


class Response(Result):
    status: int = 200
    headers: dict = {}
    body: dict = {}
