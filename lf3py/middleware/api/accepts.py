from lf3py.api.errors import NotAcceptableError
from lf3py.api.request import Request
from lf3py.openapi.schema import embed


@embed.produce('application/json')
def json(request: Request):
    if request.headers.get('Accept') != 'application/json':
        raise NotAcceptableError()
