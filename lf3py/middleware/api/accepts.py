from lf3py.api.errors import NotAcceptableError
from lf3py.api.request import Request


def json(request: Request):
    if request.headers.get('Accept') != 'application/json':
        raise NotAcceptableError()
