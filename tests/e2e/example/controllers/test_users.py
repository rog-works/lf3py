import example.preprocess  # noqa: F401

import json
import os
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
                'statusCode': 200,
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
                'statusCode': 200,
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
                'statusCode': 200,
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
            {},
            {
                'path': '/users',
                'httpMethod': 'POST',
                'headers': {'content-type': 'application/json'},
                'queryStringParameters': {'locale': 'ja'},
                'body': json.dumps({'unknown': 'piyo'}),
            },
            {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': {'message': '400 Bad Request', 'stacktrace': list},
            },
        ),
        (
            {
                'MODULES_ERROR_HANDLER': 'example.provider.error_handler.make_prd_handler',
            },
            {
                'path': '/users',
                'httpMethod': 'POST',
                'headers': {'content-type': 'application/json'},
                'queryStringParameters': {'locale': 'ja'},
                'body': json.dumps({'unknown': 'piyo'}),
            },
            {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': {'message': '400 Bad Request', 'stacktrace': type(None)},
            },
        ),
    ])
    def test_error(self, environ: dict, event: dict, expected: dict):
        with mock.patch.dict(os.environ, environ):
            actual = perform_api(event)
            self.assertEqual(actual['statusCode'], expected['statusCode'])
            self.assertEqual(actual['headers'], expected['headers'])
            self.assertEqual(actual['body']['message'], expected['body']['message'])
            self.assertTrue(type(actual['body'].get('stacktrace')) is expected['body']['stacktrace'])
