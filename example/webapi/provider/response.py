from lf2.api.data import Response
from lf2.data.config import Config


def make_response(config: Config) -> Response:
    return Response(headers=config['response']['headers'])
