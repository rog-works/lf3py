from unittest import TestCase

from framework.lang.module import load_module
from tests.helper.fixture import data_provider


class Context:
    pass


class TestModels(TestCase):
    @data_provider([
        (
            {
                'path': '/models',
                'httpMethod': 'GET',
                'headers': {},
                'queryStringParameters': {'locale': 'ja'},
            },
            {
                'status': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': {'success': True},
            },
        )
    ])
    def test_action(self, event: dict, expected: dict):
        handler = load_module('example.handler', 'handler')
        actual = handler(event, Context())
        self.assertEqual(actual, expected)
