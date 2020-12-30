from lf3py.api.errors import ApiError
from lf3py.api.response import ErrorBody, Response
from lf3py.api.symbols import IApiRender
from lf3py.lang.error import stacktrace
from lf3py.task.data import Result


class ApiRender(IApiRender):
    def __init__(self, response: Response) -> None:
        self._response = response

    def ok(self, status: int = 200, body: Result = Result()) -> Response:
        return self.http_result(status, body)

    def fail(self, error: Exception) -> Response:
        if isinstance(error, ApiError):
            return self.error_result(error.status, str(error), error)
        else:
            return self.error_result(500, '500 Internal Server Error', error)

    def http_result(self, status: int = 200, body: Result = Result()) -> Response:
        return Response(statusCode=status, headers=self._response.headers, body=body)

    def error_result(self, status: int, message: str, error: Exception) -> Response:
        return self.http_result(status, self.build_error_body(status, message, error))

    def build_error_body(self, status: int, message: str, error: Exception) -> Result:
        return ErrorBody(message=message, stacktrace=stacktrace(error))
