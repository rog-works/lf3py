import json
from io import TextIOWrapper
import re
from typing import Any, Dict, List
from urllib.parse import parse_qsl

from wsgiref.simple_server import make_server

from lf3py.aws.types import LambdaHandler
from lf3py.wsgi.types import StartResponse


class Handler:
    def __init__(self, handler: LambdaHandler) -> None:
        self._handler = handler

    def __call__(self, environ: dict, start_response: StartResponse) -> List[bytes]:
        event = RequestDecoder.decode(environ)
        response = self._handler(event, object())
        status_desciption = self.__to_status_desciption(response['statusCode'])
        headers_tuple = [(key, value) for key, value in response['headers'].items()]
        start_response(status_desciption, headers_tuple)
        return [json.dumps(response['body']).encode('utf-8')]

    def __to_status_desciption(self, status: int) -> str:
        mapping = {
            200: '200 OK',
            400: '400 Bad request',
            401: '401 Unauthorized',
            415: '415 Unsupported Media Type',
            500: '500 Internal Server Error',
            503: '503 Service Unavailable',
        }
        return mapping[status] if status in mapping else mapping[500]


class RequestDecoder:
    @classmethod
    def decode(cls, environ: dict) -> dict:
        query_params = cls.__parse_query_string(environ.get('QUERY_STRING', ''))
        headers = cls.__parse_headers(environ)
        body = cls.__parse_body(environ.get('wsgi.input', b''), headers['Content-Length'])
        return {
            'httpMethod': environ['REQUEST_METHOD'],
            'path': environ['PATH_INFO'],
            'headers': headers,
            'queryStringParameters': query_params,
            'body': body,
        }

    @classmethod
    def __parse_headers(cls, environ: dict) -> Dict[str, Any]:
        headers = {
            'Content-Type': environ.get('CONTENT_TYPE', ''),
            'Content-Length': int(environ['CONTENT_LENGTH'] if environ.get('CONTENT_LENGTH', '') != '' else 0),
        }
        matcher = re.compile(r'^HTTP_([\w\d-])$')
        for key, value in environ.items():
            matches = matcher.match(key)
            if matches:
                header_key = matches.group(1)
                headers[header_key] = value

        return headers

    @classmethod
    def __parse_query_string(cls, query_string: str) -> dict:
        return dict(parse_qsl(query_string))

    @classmethod
    def __parse_body(cls, stream: TextIOWrapper, length: int) -> str:
        return stream.read(length) if length > 0 else ''


class Server:
    def __init__(self, handler: Handler):
        self._handler = handler

    def listen(self, host: str = 'localhost', port: int = 80):
        with make_server(host, port, self._handler) as httpd:
            httpd.serve_forever()
