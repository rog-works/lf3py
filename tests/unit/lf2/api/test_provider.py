import json
from unittest import TestCase

from lf2.api.provider import request
from lf2.aws.types import LambdaEvent
from lf2.test.helper import data_provider


class TestProvider(TestCase):
    @data_provider([
        ('GET', '/', {}, {}, {}),
        ('GET', '/users', {'content-type': 'application/json'}, {'locale': 'jp'}, {}),
        ('POST', '/users', {'content-type': 'application/json'}, {'locale': 'jp'}, {'name': 'hoge'}),
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

