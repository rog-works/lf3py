from unittest import TestCase

from lf3py.test.helper import data_provider

from example.inlineapi.handler import handler


class TestHandler(TestCase):
    @data_provider([
        (
            {
                'path': '/models',
                'httpMethod': 'GET',
                'headers': {},
                'queryStringParameters': {},
            },
            {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': {
                    'models': [
                        {'id': 1234},
                    ],
                },
            },
        ),
    ])
    def test_index(self, event: dict, expected: dict):
        self.assertEqual(handler(event, object()), expected)

    @data_provider([
        (
            {
                'path': '/models/1234',
                'httpMethod': 'GET',
                'headers': {},
                'queryStringParameters': {},
            },
            {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': {
                    'model': {'id': 1234},
                },
            },
        ),
    ])
    def test_show(self, event: dict, expected: dict):
        self.assertEqual(handler(event, object()), expected)

    @data_provider([
        (
            {
                'path': '/models/hoge',
                'httpMethod': 'GET',
                'headers': {},
                'queryStringParameters': {},
            },
            {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': {
                    'message': '400 Bad Request',
                    'stacktrace': list,
                },
            },
        ),
    ])
    def test_error(self, event: dict, expected: dict):
        result = handler(event, object())
        self.assertEqual(result['statusCode'], expected['statusCode'])
        self.assertEqual(result['headers'], expected['headers'])
        self.assertEqual(result['body']['message'], expected['body']['message'])
        self.assertEqual(type(result['body']['stacktrace']), expected['body']['stacktrace'])
