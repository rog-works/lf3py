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
