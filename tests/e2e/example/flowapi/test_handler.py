from unittest import TestCase

from lf3py.api.errors.errors import ApiError
from lf3py.test.helper import data_provider

from tests.helper.example.flowapi import perform_api


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
        self.assertEqual(perform_api(event), expected)

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
        self.assertEqual(perform_api(event), expected)

    @data_provider([
        (
            {
                'path': '/models/hoge',
                'httpMethod': 'GET',
                'headers': {},
                'queryStringParameters': {},
            },
            {
                'raise': ApiError,
                'message': '400 Bad Request',
            },
        ),
    ])
    def test_error(self, event: dict, expected: dict):
        with self.assertRaisesRegex(expected['raise'], expected['message']):
            perform_api(event)
