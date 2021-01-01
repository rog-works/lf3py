from io import BytesIO
import json
from typing import Any, Callable, List, Optional, Tuple
from unittest import TestCase

from lf3py.test.helper import data_provider
from lf3py.wsgi.wsgi import Handler, RequestDecoder


class StubStartResponse:
    def __init__(self) -> None:
        self.status = ''
        self.headers = []

    def __call__(self, status: str, headers: List[Tuple[str, str]], exc_info: Optional[Any] = None) -> Callable[[bytes], Any]:
        self.status = status
        self.headers = headers
        return lambda bytes: 1234


class TestHandler(TestCase):
    @data_provider([
        (
            {
                'REQUEST_METHOD': 'GET',
                'PATH_INFO': '/',
                'CONTENT_TYPE': 'application/json',
                'CONTENT_LENGTH': '',
                'QUERY_STRING': 'lang=ja',
                'wsgi.input': b'',
            },
            {
                'status': '200 OK',
                'headers': [('Content-Type', 'application/json')],
                'body': [json.dumps({'success': True}).encode('utf-8')],
            }
        ),
    ])
    def test_call(self, environ: dict, expected: dict):
        def lambda_handler(event: dict, context: object) -> dict:
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                },
                'body': {
                    'success': True,
                },
            }

        handler = Handler(lambda_handler)
        start_response = StubStartResponse()
        body = handler(environ, start_response)
        self.assertEqual(expected['status'], start_response.status)
        self.assertEqual(expected['headers'], start_response.headers)
        self.assertEqual(expected['body'], body)


class TestRequestDecoder(TestCase):
    @data_provider([
        (
            {
                'REQUEST_METHOD': 'GET',
                'PATH_INFO': '/',
                'CONTENT_TYPE': 'application/json',
                'CONTENT_LENGTH': '',
                'QUERY_STRING': 'lang=ja',
                'wsgi.input': b'',
            },
            {
                'httpMethod': 'GET',
                'path': '/',
                'headers': {
                    'Content-Type': 'application/json',
                    'Content-Length': 0,
                },
                'queryStringParameters': {
                    'lang': 'ja',
                },
                'body': '',
            },
        ),
        (
            {
                'REQUEST_METHOD': 'POST',
                'PATH_INFO': '/models',
                'CONTENT_TYPE': 'application/json',
                'CONTENT_LENGTH': len(json.dumps({'name': 'hoge'}).encode('utf-8')),
                'QUERY_STRING': 'lang=ja&encode=utf-8',
                'wsgi.input': BytesIO(json.dumps({'name': 'hoge'}).encode('utf-8')),
            },
            {
                'httpMethod': 'POST',
                'path': '/models',
                'headers': {
                    'Content-Type': 'application/json',
                    'Content-Length': len(json.dumps({'name': 'hoge'}).encode('utf-8')),
                },
                'queryStringParameters': {
                    'lang': 'ja',
                    'encode': 'utf-8',
                },
                'body': json.dumps({'name': 'hoge'}).encode('utf-8'),
            },
        ),
    ])
    def test_decode(self, environ: dict, expected: dict):
        self.assertEqual(expected, RequestDecoder.decode(environ))
