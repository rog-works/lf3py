class Response:
    def __init__(self, status: int, body: dict, headers: dict) -> None:
        self._status = status
        self._body = body
        self._headers = headers

    @property
    def status(self) -> int:
        return self._status

    @property
    def body(self) -> dict:
        return self._body

    @property
    def headers(self) -> dict:
        return self._headers


class ErrorResponse(Response):
    def __init__(self, status: int, message: str, error: Exception) -> None:
        super().__init__(status, {}, {})
        self._message = message
        self._error = error

    @property
    def body(self) -> dict:
        return {
            'message': self._message,
            'stacktrace': self._error.__traceback__,
        }
