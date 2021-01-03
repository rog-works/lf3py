from abc import ABCMeta, abstractmethod

from lf3py.task.data import Result


class IRender(metaclass=ABCMeta):
    @abstractmethod
    def ok(self, *args, **kwargs) -> Result:
        raise NotImplementedError()

    @abstractmethod
    def fail(self, *args, **kwargs) -> Result:
        raise NotImplementedError()
