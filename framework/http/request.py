class Request:
    def __init__(self, path: str, method: str, headers: dict, params: dict) -> None:
        self._path = path
        self._method = method
        self._headers = headers
        self._params = params

    @property
    def path(self) -> str:
        return self._path

    @property
    def method(self) -> str:
        return self._method

    @property
    def headers(self) -> dict:
        return self._headers

    @property
    def params(self) -> dict:
        return self._params
