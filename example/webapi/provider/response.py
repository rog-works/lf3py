import uuid

from lf2.api.data import Response


def make_response() -> Response:
    return Response(headers={'X-Correlation-Id': str(uuid.uuid4())})
