import json

import boto3


class FireHose:
    def __init__(self, delivery_stream_name: str) -> None:
        self._delivery_stream_name = delivery_stream_name
        self._client = boto3.client('firehose')

    def put(self, payload: dict):
        data = json.dumps(payload)
        self._client.put_record(
            DeliveryStreamName=self._delivery_stream_name,
            Data=f'{data}\n',
        )
