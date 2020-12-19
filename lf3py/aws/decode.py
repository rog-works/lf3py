from base64 import b64decode
import json
from urllib.parse import parse_qsl

from lf3py.aws.types import LambdaEvent


def decode_request(event: LambdaEvent) -> dict:
    return {
        'path': event['path'],
        'method': event['httpMethod'],
        'headers': event['headers'],
        'params': {**event.get('queryStringParameters', {}), **__decode_body(event)},
    }


def __decode_body(event: LambdaEvent) -> dict:
    if 'body' not in event:
        return {}

    content_type = event['headers'].get('content-type', '')
    if content_type.find('application/json') != -1:
        return json.loads(event['body'])
    elif content_type.find('application/x-www-form-urlencoded') != -1:
        return dict(parse_qsl(b64decode(event['body']).decode('utf-8')))
    else:
        return {}
