import json
from unittest import TestCase, mock

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
                'body': {
                    'success': True,
                    'users': [
                        {'id': 1, 'name': 'hoge'},
                        {'id': 2, 'name': 'fuga'},
                    ],
                },
            },
        ),
    ])
    def test_index(self, event: dict, expected: dict):
        with mock.patch('example.repos.user_repo.UserRepo.find_all') as p:
            p.return_value = [
                {'id': 1, 'name': 'hoge'},
                {'id': 2, 'name': 'fuga'},
            ]
            self.assertEqual(perform_api(event), expected)

    @data_provider([
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
    ])
    def test_show(self, event: dict, expected: dict):
        with mock.patch('example.repos.user_repo.UserRepo.find') as p:
            p.return_value = {'id': 1234, 'name': 'hoge'}
            self.assertEqual(perform_api(event), expected)

    @data_provider([
        (
            {
                'path': '/users',
                'httpMethod': 'POST',
                'headers': {'content-type': 'application/json'},
                'queryStringParameters': {'locale': 'ja'},
                'body': json.dumps({'name': 'piyo'}),
            },
            {
                'status': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': {'success': True, 'user': {'id': 100, 'name': 'piyo'}},
            },
        ),
    ])
    def test_create(self, event: dict, expected: dict):
        with mock.patch('example.repos.user_repo.UserRepo.create') as p:
            p.return_value = {'id': 100, 'name': 'piyo'}
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
