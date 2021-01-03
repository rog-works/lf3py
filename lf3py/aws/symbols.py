from abc import ABCMeta, abstractmethod


class IFireHose(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, delivery_stream_name: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def put(self, payload: dict):
        raise NotImplementedError()
