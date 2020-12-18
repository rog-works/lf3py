import json
from unittest import TestCase

from lf2.api.request import Request
from lf2.aws.types import LambdaEvent
from lf2.test.helper import data_provider


class TestRequest(TestCase):
    @data_provider([
        ('GET', '/', {}, {}, {}),
        ('GET', '/users', {'content-type': 'application/json'}, {'locale': 'jp'}, {}),
        ('POST', '/users', {'content-type': 'application/json'}, {'locale': 'jp'}, {'name': 'hoge'}),
    ])
    def test_from_event(self, method: str, path: str, headers: dict, query: dict, body: dict):
        event = LambdaEvent(
            httpMethod=method,
            path=path,
            headers=headers,
            queryStringParameters=query,
            body=json.dumps(body),
        )
        request = Request.from_event(event)
        self.assertEqual(request.method, method)
        self.assertEqual(request.path, path)
        self.assertEqual(request.headers, headers)
        self.assertEqual(request.params, {**query, **body})
