from lf3py.api.errors import UnsupportedMediaTypeError
from lf3py.api.request import Request


def json(request: Request):
    if request.headers.get('Content-Type') != 'application/json':
        raise UnsupportedMediaTypeError()
