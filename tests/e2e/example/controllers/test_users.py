import json
from unittest import TestCase

from framework.test.helper import data_provider
from tests.helper.example import perform_api


class TestUsers(TestCase):
    @data_provider([
        (
            {
                'path': '/users',
                'httpMethod': 'GET',
                'headers': {},
                'queryStringParameters': {'locale': 'ja'},
            },
            {
                'status': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': {'success': True, 'users': []},
            },
        ),
        (
            {
                'path': '/users/1234',
                'httpMethod': 'GET',
                'headers': {},
                'queryStringParameters': {'locale': 'ja'},
            },
            {
                'status': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': {'success': True, 'user': {'id': 1234, 'name': 'hoge'}},
            },
        ),
        (
            {
                'path': '/users',
                'httpMethod': 'POST',
                'headers': {'content-type': 'application/json'},
                'queryStringParameters': {'locale': 'ja'},
                'body': json.dumps({'name': 'fuga'}),
            },
            {
                'status': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': {'success': True, 'user': {'id': 1, 'name': 'fuga'}},
            },
        ),
    ])
    def test_action(self, event: dict, expected: dict):
        self.assertEqual(perform_api(event), expected)

    @data_provider([
        (
            {
                'path': '/users',
                'httpMethod': 'POST',
                'headers': {'content-type': 'application/json'},
                'queryStringParameters': {'locale': 'ja'},
                'body': json.dumps({'unknown': 'piyo'}),
            },
            {
                'status': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': {'message': '400 Bad Request', 'stacktrace': []},
            },
        ),
    ])
    def test_error(self, event: dict, expected: dict):
        actual = perform_api(event)
        self.assertEqual(actual['status'], expected['status'])
        self.assertEqual(actual['headers'], expected['headers'])
        self.assertEqual(actual['body']['message'], expected['body']['message'])
        self.assertTrue(type(actual['body']['stacktrace']) is list)
