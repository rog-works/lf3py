from dataclasses import dataclass


@dataclass
class Request:
    path: str = ''
    method: str = ''
    headers: dict = {}
    params: dict = {}


@dataclass
class Response:
    status: int = 0
    headers: dict = {}
    body: dict = {}


@dataclass
class ErrorResponse(Response):
    message: str = ''
    error: Exception = Exception()
