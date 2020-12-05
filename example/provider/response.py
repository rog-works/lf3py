from typing import Any

from framework.lang.serialize import DictSerializer
from framework.api.data import Response
from framework.data.config import Config
from framework.lang.module import load_module


def make_response(config: Config) -> Response:
    func_name = config['response']['module']
    func_args = config['response']['modules'][func_name]
    return load_module(__name__, func_name)(**func_args)


def dev_response(headers: dict) -> Response:
    return Response(headers=headers)


def prd_response(headers: dict) -> Response:
    return Response(headers=headers, _serializer=SafeDictSerializer())


class SafeDictSerializer(DictSerializer):
    def serialize(self, obj: Any) -> dict:
        serialized = super().serialize(obj)
        if type(obj) is Response and 'stacktrace' in serialized['body']:
            del serialized['body']['stacktrace']

        return serialized
