from lf3py.api.errors import UnsupportedMediaTypeError
from lf3py.api.request import Request


def accept_json(request: Request):
    if request.headers.get('Accept') != 'application/json':
        raise UnsupportedMediaTypeError()
