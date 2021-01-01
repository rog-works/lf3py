from io import BytesIO
import json
from unittest import TestCase

from lf3py.test.helper import data_provider
from lf3py.wsgi.wsgi import RequestDecoder


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
