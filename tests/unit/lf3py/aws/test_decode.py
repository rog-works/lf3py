import base64
import json
from unittest import TestCase
import urllib.parse

from lf3py.aws.decode import decode_request
from lf3py.aws.types import LambdaEvent
from lf3py.test.helper import data_provider


class TestDecode(TestCase):
    @data_provider([
        (
            {
                'requestContext': {},
                'httpMethod': 'GET',
                'path': '/models',
                'queryStringParameters': {'locale': 'ja'},
                'headers': {},
                'body': ''
            },
            {
                'path': '/models',
                'method': 'GET',
                'headers': {},
                'params': {'locale': 'ja'},
            },
        ),
        (
            {
                'requestContext': {},
                'httpMethod': 'POST',
                'path': '/models',
                'queryStringParameters': {'locale': 'ja'},
                'headers': {'Content-Type': 'application/json; charset=utf-8'},
                'body': json.dumps({'type': 1234, 'name': 'ほ げ', 'json': '{"hoge":"fuga"}'})
            },
            {
                'path': '/models',
                'method': 'POST',
                'headers': {'Content-Type': 'application/json; charset=utf-8'},
                'params': {'locale': 'ja', 'type': 1234, 'name': 'ほ げ', 'json': '{"hoge":"fuga"}'},
            },
        ),
        (
            {
                'requestContext': {},
                'httpMethod': 'POST',
                'path': '/models',
                'queryStringParameters': {'locale': 'ja'},
                'headers': {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'},
                'body': base64.b64encode(urllib.parse.urlencode({'model_id': 1234, 'name': 'ほ げ', 'json': '{"hoge":"fuga"}'}).encode('utf-8')),
            },
            {
                'path': '/models',
                'method': 'POST',
                'headers': {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'},
                'params': {'locale': 'ja', 'model_id': '1234', 'name': 'ほ げ', 'json': '{"hoge":"fuga"}'},
            },
        ),
    ])
    def test_decode_request(self, event: LambdaEvent, expected: dict):
        request = decode_request(event)
        self.assertEqual(request, expected)
