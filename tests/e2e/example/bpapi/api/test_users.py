import example.bpapi.preprocess  # noqa: F401

import json
import os
from unittest import TestCase, mock

from lf3py.test.helper import data_provider

from example.bpapi.handler import handler


class TestUsers(TestCase):
    @data_provider([
        (
            {
                'path': '/users',
                'httpMethod': 'GET',
                'headers': {
                    'Accept': 'application/json',
                },
                'queryStringParameters': {'locale': 'ja'},
            },
            {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'X-Correlation-Id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
                },
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
        with mock.patch('uuid.uuid4') as p:
            p.return_value = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
            with mock.patch('example.bpapi.repos.user_repo.UserRepo.find_all') as p2:
                p2.return_value = [
                    {'id': 1, 'name': 'hoge'},
                    {'id': 2, 'name': 'fuga'},
                ]
                self.assertEqual(handler(event, object()), expected)

    @data_provider([
        (
            {
                'path': '/users/1234',
                'httpMethod': 'GET',
                'headers': {
                    'Accept': 'application/json',
                },
                'queryStringParameters': {'locale': 'ja'},
            },
            {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'X-Correlation-Id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
                },
                'body': {'success': True, 'user': {'id': 1234, 'name': 'hoge'}},
            },
        ),
    ])
    def test_show(self, event: dict, expected: dict):
        with mock.patch('uuid.uuid4') as p:
            p.return_value = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
            with mock.patch('example.bpapi.repos.user_repo.UserRepo.find') as p2:
                p2.return_value = {'id': 1234, 'name': 'hoge'}
                self.assertEqual(handler(event, object()), expected)

    @data_provider([
        (
            {
                'path': '/users',
                'httpMethod': 'POST',
                'headers': {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                'queryStringParameters': {'locale': 'ja'},
                'body': json.dumps({'name': 'piyo'}),
            },
            {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'X-Correlation-Id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
                },
                'body': {'success': True, 'user': {'id': 100, 'name': 'piyo'}},
            },
        ),
    ])
    def test_create(self, event: dict, expected: dict):
        with mock.patch('uuid.uuid4') as p:
            p.return_value = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
            with mock.patch('example.bpapi.repos.user_repo.UserRepo.create') as p2:
                p2.return_value = {'id': 100, 'name': 'piyo'}
                self.assertEqual(handler(event, object()), expected)

    @data_provider([
        (
            {},
            {
                'path': '/users',
                'httpMethod': 'POST',
                'headers': {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                'queryStringParameters': {'locale': 'ja'},
                'body': json.dumps({'unknown': 'piyo'}),
            },
            {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'X-Correlation-Id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
                },
                'body': {
                    'message': '400 Bad Request',
                    'stacktrace': list,
                },
            },
        ),
        (
            {
                'MODULES_RENDER': 'example.bpapi.api.error.SafeApiRender',
            },
            {
                'path': '/users',
                'httpMethod': 'POST',
                'headers': {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                'queryStringParameters': {'locale': 'ja'},
                'body': json.dumps({'unknown': 'piyo'}),
            },
            {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'X-Correlation-Id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
                },
                'body': {
                    'message': '400 Bad Request',
                    'stacktrace': type(None),
                },
            },
        ),
    ])
    def test_error(self, environ: dict, event: dict, expected: dict):
        with mock.patch('uuid.uuid4') as p:
            p.return_value = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
            with mock.patch.dict(os.environ, environ):
                result = handler(event, object())
                self.assertEqual(result['statusCode'], expected['statusCode'])
                self.assertEqual(result['headers'], expected['headers'])
                self.assertEqual(result['body']['message'], expected['body']['message'])
                self.assertEqual(type(result['body'].get('stacktrace')), expected['body']['stacktrace'])
