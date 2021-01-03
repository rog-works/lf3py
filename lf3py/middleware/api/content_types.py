from lf3py.api.errors import UnsupportedMediaTypeError
from lf3py.api.request import Request
from lf3py.openapi.schema import embed


@embed.consume('application/json')
def json(request: Request):
    if request.headers.get('Content-Type') != 'application/json':
        raise UnsupportedMediaTypeError()
