import json
from unittest import TestCase

from lf3py.api.provider import request
from lf3py.aws.types import LambdaEvent
from lf3py.test.helper import data_provider


class TestProvider(TestCase):
    @data_provider([
        ('GET', '/', {}, {}, {}),
        ('GET', '/users', {'Content-Type': 'application/json'}, {'locale': 'jp'}, {}),
        ('POST', '/users', {'Content-Type': 'application/json'}, {'locale': 'jp'}, {'name': 'hoge'}),
    ])
    def test_request(self, method: str, path: str, headers: dict, query: dict, body: dict):
        event = LambdaEvent(
            httpMethod=method,
            path=path,
            headers=headers,
            queryStringParameters=query,
            body=json.dumps(body),
        )
        actual = request(event)
        self.assertEqual(actual.method, method)
        self.assertEqual(actual.path, path)
        self.assertEqual(actual.headers, headers)
        self.assertEqual(actual.params, {**query, **body})

