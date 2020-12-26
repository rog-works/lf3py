from base64 import b64decode
import json
from typing import Dict
from urllib.parse import parse_qsl

from lf3py.aws.types import LambdaEvent


def decode_request(event: LambdaEvent) -> dict:
    headers = __decode_headers(event['headers'])
    query_params = event.get('queryStringParameters', {})
    body = __decode_body(event.get('body', ''), headers)
    return {
        'path': event['path'],
        'method': event['httpMethod'],
        'headers': headers,
        'params': {**query_params, **body},
    }


def __decode_headers(headers: Dict[str, str]) -> dict:
    def camelize(key: str) -> str:
        return '-'.join(map(lambda k: k[0].upper() + k[1:], key.split('-')))

    return {camelize(key): value for key, value in headers.items()}


def __decode_body(body: str, headers: Dict[str, str]) -> dict:
    if not body:
        return {}

    content_type = headers.get('Content-Type', '')
    if content_type.find('application/json') != -1:
        return json.loads(body)
    elif content_type.find('application/x-www-form-urlencoded') != -1:
        return dict(parse_qsl(b64decode(body).decode('utf-8')))
    else:
        return {}
