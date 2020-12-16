import example.webapi.preprocess  # noqa: F401

import json
import os
from unittest import TestCase, mock

from lf2.api.errors import ApiError
from lf2.test.helper import data_provider

from tests.helper.example.webapi import perform_api


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
            with mock.patch('example.webapi.repos.user_repo.UserRepo.find_all') as p2:
                p2.return_value = [
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
            with mock.patch('example.webapi.repos.user_repo.UserRepo.find') as p2:
                p2.return_value = {'id': 1234, 'name': 'hoge'}
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
            with mock.patch('example.webapi.repos.user_repo.UserRepo.create') as p2:
                p2.return_value = {'id': 100, 'name': 'piyo'}
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
                'raise': ApiError,
                'message': '400 Bad Request',
            },
        ),
        (
            {
                'MODULES_RENDER': 'example.webapi.api.error.SafeApiRender',
            },
            {
                'path': '/users',
                'httpMethod': 'POST',
                'headers': {'content-type': 'application/json'},
                'queryStringParameters': {'locale': 'ja'},
                'body': json.dumps({'unknown': 'piyo'}),
            },
            {
                'raise': ApiError,
                'message': '400 Bad Request',
            },
        ),
    ])
    def test_error(self, environ: dict, event: dict, expected: dict):
        with mock.patch('uuid.uuid4') as p:
            p.return_value = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
            with mock.patch.dict(os.environ, environ):
                with self.assertRaisesRegex(expected['raise'], expected['message']):
                    perform_api(event)
