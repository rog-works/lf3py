from lf3py.errors import Error


class ApiError(Error):
    def __init__(self, message: str, status: int) -> None:
        super(ApiError, self).__init__(message)
        self.status = status


class HTTPError(Error): pass
class BadRequestError(HTTPError): pass
class UnauthorizedError(HTTPError): pass
class ForbiddenError(HTTPError): pass
class DataNotFoundError(HTTPError): pass
class UnsupportedMediaTypeError(HTTPError): pass
class InternalServerError(HTTPError): pass
class ServiceUnavailableError(HTTPError): pass
