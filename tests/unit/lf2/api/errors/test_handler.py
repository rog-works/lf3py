from typing import List, Type
from unittest import TestCase

from lf2.api.errors import ApiError, BadRequestError, InternalServerError
from lf2.api.errors.handler import ApiErrorHandler
from lf2.api.errors.types import ErrorDefinition
from lf2.task.result import Result
from lf2.test.helper import data_provider


class TestApiErrorHandler(TestCase):
    @data_provider([
        (400, '400 Bad Request', BadRequestError),
    ])
    def test_call(self, status: int, message: str, handle_error: Type[Exception]):
        error = ApiErrorHandler()

        @error(status, message, handle_error)
        def func() -> Result:
            raise BadRequestError()

        with self.assertRaisesRegex(ApiError, message):
            func()

    @data_provider([
        (400, '400 Bad Request', BadRequestError),
    ])
    def test_define(self, status: int, message: str, handle_error: Type[Exception]):
        error = ApiErrorHandler()
        definition = error.define(status, message, handle_error)
        self.assertEqual(type(definition), tuple)
        self.assertEqual(status, definition[0])
        self.assertEqual(message, definition[1])
        self.assertEqual((handle_error,), definition[2])

    @data_provider([
        (BadRequestError, '400 Bad Request'),
        (InternalServerError, '500 Internal Server Error'),
    ])
    def test_custom(self, raise_error: Type[Exception], expected_message: str):
        error = ApiErrorHandler()

        @error.custom
        def custom_error() -> List[ErrorDefinition]:
            return [
                error.define(400, '400 Bad Request', BadRequestError),
                error.define(500, '500 Internal Server Error', InternalServerError),
            ]

        @custom_error()
        def func() -> Result:
            raise raise_error()

        with self.assertRaisesRegex(ApiError, expected_message):
            func()

    @data_provider([
        (BadRequestError, '400 Bad Request'),
        (InternalServerError, '500 Internal Server Error'),
    ])
    def test_handles(self, raise_error: Type[Exception], expected_message: str):
        error = ApiErrorHandler()

        @error.handles([
            error.define(400, '400 Bad Request', BadRequestError),
            error.define(500, '500 Internal Server Error', InternalServerError),
        ])
        def func() -> Result:
            raise raise_error()

        with self.assertRaisesRegex(ApiError, expected_message):
            func()
