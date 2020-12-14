from lf2.api.errors import ApiError
from lf2.api.data import ErrorBody, Response
from lf2.lang.error import stacktrace
from lf2.task.result import Result
from lf2.view.render import Render


class ApiRender(Render):
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
