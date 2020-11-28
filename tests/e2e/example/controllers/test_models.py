from unittest import TestCase

from example.provider import aws_app
from framework.lang.module import unload_module
from tests.helper.fixture import data_provider


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
        ),
        (
            {
                'path': '/models/1234',
                'httpMethod': 'GET',
                'headers': {},
                'queryStringParameters': {'locale': 'ja'},
            },
            {
                'status': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': {'success': True, 'id': 1234},
            },
        ),
    ])
    def test_action(self, event: dict, expected: dict):
        app = aws_app(event, object())
        actual = app.run().serialize()
        self.assertEqual(actual, expected)
        unload_module(app.runner.__module__)
