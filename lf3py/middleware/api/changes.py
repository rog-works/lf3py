from lf3py.api.errors import BadRequestError
from lf3py.routing.errors import DispatchError


def fail_dispach_to_400(error: Exception, *args):
    if isinstance(error, DispatchError):
        raise BadRequestError() from error
