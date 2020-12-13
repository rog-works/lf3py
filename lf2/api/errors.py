from lf2.errors import Error


class HTTPError(Error): pass  # noqa: E701
class BadRequestError(HTTPError): pass  # noqa: E701
class UnauthorizedError(HTTPError): pass  # noqa: E701
class InternalServerError(HTTPError): pass  # noqa: E701
class ServiceUnavailableError(HTTPError): pass  # noqa: E701
