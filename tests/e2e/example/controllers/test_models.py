from unittest import TestCase

from example.provider import aws_app
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
        )
    ])
    def test_action(self, event: dict, expected: dict):
        app = aws_app(event, object())
        actual = app.run().serialize()
        self.assertEqual(actual, expected)
