from lf2.task.result import Result


class Presenter:
    def __call__(self, *args, **kwargs) -> Result:
        raise NotImplementedError()
