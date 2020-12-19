from unittest import TestCase

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
