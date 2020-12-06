from framework.api.data import Response
from framework.data.config import Config


def make_response(config: Config) -> Response:
    return Response(headers=config['response']['headers'])
