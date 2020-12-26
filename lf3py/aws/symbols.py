from abc import ABCMeta


class IFireHose(metaclass=ABCMeta):
    def __init__(self, delivery_stream_name: str) -> None:
        raise NotImplementedError()

    def put(self, payload: dict):
        raise NotImplementedError()
