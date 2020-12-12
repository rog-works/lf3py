from lf2.errors import Error


class BadRequestError(Error): pass  # noqa: E701
class UnauthorizeError(Error): pass  # noqa: E701
class ServiceUnavailableError(Error): pass  # noqa: E701
