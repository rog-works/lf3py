from unittest import TestCase

from lf3py.api.errors import ApiError
from lf3py.api.render import ApiRender
from lf3py.api.response import Response
from lf3py.test.helper import data_provider


class TestRender(TestCase):
    @data_provider([
        (200, {'statusCode': 200, 'headers': {'Content-Type': 'application/json'}, 'body': {}}),
    ])
    def test_ok(self, status: int, expected: dict):
        render = ApiRender(Response())
        actual = render.ok(status=status).json().serialize()
        self.assertEqual(actual, expected)

    @data_provider([
        (
            ApiError('400 Bad Request', 400),
            {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': {
                    'message': '400 Bad Request',
                    'stacktrace': ['lf3py.api.errors.errors.ApiError: 400 Bad Request\n'],
                },
            }
        ),
        (
            Exception('Error'),
            {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': {
                    'message': '500 Internal Server Error',
                    'stacktrace': ['Exception: Error\n'],
                },
            }
        ),
    ])
    def test_fail(self, error: Exception, expected: dict):
        render = ApiRender(Response())
        actual = render.fail(error).json().serialize()
        self.assertEqual(actual, expected)
