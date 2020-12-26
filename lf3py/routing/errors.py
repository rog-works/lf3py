from lf3py.errors import Error


class RoutingError(Error): pass
class RouteMismatchError(RoutingError): pass
class DispatchError(RoutingError): pass
class UnexpectedDispatchError(DispatchError): pass
class UnresolvedArgumentsError(DispatchError): pass
