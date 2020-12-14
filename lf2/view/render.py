from abc import ABCMeta

from lf2.task.result import Result


class Render(metaclass=ABCMeta):
    def ok(self, *args, **kwargs) -> Result:
        raise NotImplementedError()

    def fail(self, *args, **kwargs) -> Result:
        raise NotImplementedError()
