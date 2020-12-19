from lf2.api.response import Response

from example.webapi.data.context import MyContext


def make_response(context: MyContext) -> Response:
    return Response(headers={'X-Correlation-Id': context['correlation_id']})
