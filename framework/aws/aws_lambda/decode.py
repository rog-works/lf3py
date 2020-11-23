from base64 import b64decode
import json
from urllib.parse import parse_qsl


from framework.http.data import Request


def decode_request(event: dict) -> Request:
    return Request(
        path=event['path'],
        method=event['httpMethod'],
        headers=event['headers'],
        params={**event['queryStringParameters'], **__decode_body(event)},
    )


def __decode_body(event: dict) -> dict:
    content_type = event['headers'].get('content-type', '')
    if content_type.find('application/json') != -1:
        return json.loads(event['body'])
    elif content_type.find('application/x-www-form-urlencoded') != -1:
        return dict(parse_qsl(b64decode(event['body']).decode('utf-8')))
    else:
        return {}
