from lf2.errors import Error


class ApiError(Error):
    def __init__(self, message: str, status: int) -> None:
        super(ApiError, self).__init__(message)
        self.status = status


class HTTPError(Error): pass  # noqa: E701
class BadRequestError(HTTPError): pass  # noqa: E701
class UnauthorizedError(HTTPError): pass  # noqa: E701
class InternalServerError(HTTPError): pass  # noqa: E701
class ServiceUnavailableError(HTTPError): pass  # noqa: E701
