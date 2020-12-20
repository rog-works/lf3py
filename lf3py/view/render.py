from abc import ABCMeta

from lf3py.task.data import Result


class IRender(metaclass=ABCMeta):
    def ok(self, *args, **kwargs) -> Result:
        raise NotImplementedError()

    def fail(self, *args, **kwargs) -> Result:
        raise NotImplementedError()
