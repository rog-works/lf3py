from framework.http.data import Request


def decode_request(event: dict) -> Request:
    return Request(
        path=event['path'],
        method=event['httpMethod'],
        headers=event['headers'],
        params={**event['queryStringParameters'], **event['body']},
    )
